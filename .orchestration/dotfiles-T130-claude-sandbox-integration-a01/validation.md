# T130 validation

Task source/copy SHA256: 45ebc0fdb2893852cf1769a44b0f54d7a1bbce823f400713a1050b23064fd52f
Baseline: ce032e14830b125f677a83c383986e02084bb597
Branch: feat/claude-sandbox-integration

## Before editing

```text
$ git fetch https://github.com/mryfmo/dotfiles main:refs/remotes/origin/main
(exit 0; no stdout)
$ gh api repos/shuntaka9576/blocc/releases/latest --jq .tag_name
v0.6.0
(exit 0)
$ git switch -c feat/claude-sandbox-integration --no-track origin/main
Switched to a new branch 'feat/claude-sandbox-integration'
error: Unable to create '<HOME>/Workspace/dotfiles/.git/packed-refs.lock': Operation not permitted
error: Unable to create '<HOME>/Workspace/dotfiles/.git/packed-refs.lock': Operation not permitted
(exit 0; no outside retry)
```

## Official VERIFY

URL: https://code.claude.com/docs/en/sandboxing ; fetched 2026-10-17T12:40:13.673874+00:00 with the web fetch tool. The admin-required settings table explicitly lists `network.allowMachLookup` (the dispatched spelling matches). Quote of the key: "network.allowMachLookup". The complete reference page fetch was too large; its markdown form was unsupported by the web tool; no shell fetch workaround was used.

The exclusions rule says: "where a pattern with no wildcard is an exact match." It also says: "End the pattern with ` *`". Thus agmsg-dispatch needs a trailing wildcard; the absolute script first word needs the same wildcard. This is a text match, so a tilde spelling alone cannot cover a differently expanded absolute path; render the machine home path with chezmoi. These are documentation-derived conclusions; no live apply or seat probe.

## per-os-and-forbidden-red

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form -v
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... 
  test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) (os='darwin') ... FAIL
  test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) (os='linux') ... FAIL
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... 
  test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='macOS gh exclusion') ... FAIL
  test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='Mach allowlist') ... FAIL
  test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='all Unix sockets') ... FAIL
  test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='cafe.github.com') ... FAIL
  test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='datadoghq.com') ... FAIL
  test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='api.datadoghq.com') ... FAIL
  test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='checkpoint-api.hashicorp.com') ... FAIL
  test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='api.anthropic.com') ... FAIL

======================================================================
FAIL: test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) (os='darwin')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 688, in test_claude_sandbox_renders_per_os_from_the_manifest
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        ["com.apple.trustd.agent"] if os_name == "darwin" else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        sandbox["network"].get("allowMachLookup", []),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['com.apple.trustd.agent'] != []

First list contains 1 additional elements.
First extra element 0:
'com.apple.trustd.agent'

- ['com.apple.trustd.agent']
+ []

======================================================================
FAIL: test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) (os='linux')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 697, in test_claude_sandbox_renders_per_os_from_the_manifest
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        roots + extras + (["~/Library/Caches/mise"] if os_name == "darwin" else []),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        sandbox["filesystem"]["allowWrite"],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['/re[162 chars]ls', '~/.cache/uv', '~/.local/state/mise', '~/.local/share/uv'] != ['/re[162 chars]ls', '~/.cache/uv']

First list contains 2 additional elements.
First extra element 5:
'~/.local/state/mise'

  ['/render-home/.agents/skills/agmsg/db',
   '/render-home/.agents/skills/agmsg/teams',
   '/render-home/.agents/skills/agmsg/run',
   '/render-home/.agents/skills/agmsg/ext-tools',
-  '~/.cache/uv',
?               ^

+  '~/.cache/uv']
?               ^

-  '~/.local/state/mise',
-  '~/.local/share/uv']

======================================================================
FAIL: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='macOS gh exclusion')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1096, in test_claude_sandbox_validator_refuses_each_forbidden_form
    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

======================================================================
FAIL: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='Mach allowlist')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1096, in test_claude_sandbox_validator_refuses_each_forbidden_form
    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

======================================================================
FAIL: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='all Unix sockets')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1096, in test_claude_sandbox_validator_refuses_each_forbidden_form
    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

======================================================================
FAIL: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='cafe.github.com')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1096, in test_claude_sandbox_validator_refuses_each_forbidden_form
    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

======================================================================
FAIL: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='datadoghq.com')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1096, in test_claude_sandbox_validator_refuses_each_forbidden_form
    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

======================================================================
FAIL: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='api.datadoghq.com')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1096, in test_claude_sandbox_validator_refuses_each_forbidden_form
    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

======================================================================
FAIL: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='checkpoint-api.hashicorp.com')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1096, in test_claude_sandbox_validator_refuses_each_forbidden_form
    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

======================================================================
FAIL: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='api.anthropic.com')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1096, in test_claude_sandbox_validator_refuses_each_forbidden_form
    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

----------------------------------------------------------------------
Ran 2 tests in 0.106s

FAILED (failures=10)
(exit 1)
```

## per-os-and-forbidden-green

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form -v
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.106s

OK
(exit 0)
```

## Amendment1

Full amended task read and task.md copied byte-identically; SHA256 525e493b2aa2cdd7a0a426302cd446bcbdc13f5cb6fc9537aeae86be236cf1c8. Statusline render-before-parse and production modifier host-OS rendering plus one two-OS regression are now authorized; no preceding edits to those paths.

## generate

```text
$ uv run --offline --no-project --with pyyaml scripts/generate-agent-configs.py
generated agent configs updated
(exit 0)
```

## modifier-os-red

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging -v
test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) ... 
  test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) (os='Darwin') ... ERROR
  test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) (os='Linux') ... ERROR

======================================================================
ERROR: test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) (os='Darwin')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_claude_settings_merge.py", line 547, in test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging
    result = subprocess.run(
        [sys.executable, "-c", command, os_name, str(MERGE_SCRIPT)],
        input=current, text=True, capture_output=True, env=env, check=True,
    )
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/subprocess.py", line 692, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['/tmp/codex-worker-e-uv-cache/builds-v0/.tmpXFn18f/bin/python', '-c', "import platform,runpy,sys; platform.system=lambda:sys.argv[1]; runpy.run_path(sys.argv[2],run_name='__main__')", 'Darwin', '<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json']' returned non-zero exit status 1.

======================================================================
ERROR: test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) (os='Linux')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_claude_settings_merge.py", line 547, in test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging
    result = subprocess.run(
        [sys.executable, "-c", command, os_name, str(MERGE_SCRIPT)],
        input=current, text=True, capture_output=True, env=env, check=True,
    )
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/subprocess.py", line 692, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['/tmp/codex-worker-e-uv-cache/builds-v0/.tmpXFn18f/bin/python', '-c', "import platform,runpy,sys; platform.system=lambda:sys.argv[1]; runpy.run_path(sys.argv[2],run_name='__main__')", 'Linux', '<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json']' returned non-zero exit status 1.

----------------------------------------------------------------------
Ran 1 test in 0.124s

FAILED (errors=2)
(exit 1)
```

## modifier-os-red-diagnostic

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging -v
test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) ... 
  test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) (os='Darwin') ... FAIL
  test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) (os='Linux') ... FAIL

======================================================================
FAIL: test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) (os='Darwin')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_claude_settings_merge.py", line 551, in test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging
    self.assertEqual(result.returncode, 0, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import platform,runpy,sys; platform.system=lambda:sys.argv[1]; runpy.run_path(sys.argv[2],run_name='__main__')
                                                                   ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen runpy>", line 292, in run_path
  File "<frozen runpy>", line 97, in _run_module_code
  File "<frozen runpy>", line 87, in _run_code
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json", line 214, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json", line 188, in main
    managed = json.loads(render_managed_template(baseline.read_text()))
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/__init__.py", line 371, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 358, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 374, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 67 column 15 (char 1905)


======================================================================
FAIL: test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) (os='Linux')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_claude_settings_merge.py", line 551, in test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging
    self.assertEqual(result.returncode, 0, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import platform,runpy,sys; platform.system=lambda:sys.argv[1]; runpy.run_path(sys.argv[2],run_name='__main__')
                                                                   ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen runpy>", line 292, in run_path
  File "<frozen runpy>", line 97, in _run_module_code
  File "<frozen runpy>", line 87, in _run_code
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json", line 214, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json", line 188, in main
    managed = json.loads(render_managed_template(baseline.read_text()))
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/__init__.py", line 371, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 358, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 374, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 67 column 15 (char 1905)


----------------------------------------------------------------------
Ran 1 test in 0.096s

FAILED (failures=2)
(exit 1)
```

## format

```text
$ uv run --offline --no-project --with ruff ruff format scripts/generate-agent-configs.py scripts/validate-agent-assets.py tests/unit/test_generate_agent_configs.py tests/unit/test_validate_agent_assets.py tests/unit/test_claude_settings_merge.py tests/unit/test_statusline_tools.py
5 files reformatted, 1 file left unchanged
(exit 0)
```

## connected-tests

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets tests.unit.test_claude_settings_merge tests.unit.test_statusline_tools -v
test_a_declare_r_assignment_must_appear_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_command_hooks_render_after_permission_request_in_manifest_order (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_command_hooks_render_after_permission_request_in_manifest_order) ... ok
test_codex_config_renders_permgate_permission_request (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_empty_or_missing_codex_command_hooks_render_no_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_empty_or_missing_codex_command_hooks_render_no_table) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_hook_trust_hash_reproduces_codex_current_hashes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_hook_trust_hash_reproduces_codex_current_hashes) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb) ... ok
test_managed_codex_path_includes_installed_common_bin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_orchestrator_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_orchestrator_kind) ... ok
test_model_profiles_env_renders_worker_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_env_selects_no_github_store (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_selects_no_github_store) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_orchestrator_kind_defaults_to_claude (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_orchestrator_kind_defaults_to_claude) ... ok
test_plugin_versions_order_build_metadata_like_the_semver_crate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_plugin_versions_order_build_metadata_like_the_semver_crate) ... ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_handle_table_headers_with_trailing_comments (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_handle_table_headers_with_trailing_comments) ... ok
test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin) ... ok
test_profile_modify_scripts_hash_the_plugin_version_codex_loads (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_the_plugin_version_codex_loads) ... ok
test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings) ... ok
test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_replace_a_single_quoted_declared_entry (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_a_single_quoted_declared_entry) ... ok
test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root) ... ok
test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared) ... ok
test_profile_modify_scripts_replace_inline_table_and_dotted_forms (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_inline_table_and_dotted_forms) ... ok
test_profile_modify_scripts_seed_base_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_project_map_reload_hook_accepts_only_cdp_target_ids (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_accepts_only_cdp_target_ids) ... ok
test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) ... ok
test_project_map_reload_hook_guards_against_a_tab_navigating_away (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_guards_against_a_tab_navigating_away) ... ok
test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) ... ok
test_project_map_reload_hook_pins_the_bound_tab_when_it_closes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_pins_the_bound_tab_when_it_closes) ... ok
test_project_map_reload_hook_renders_into_post_tool_use (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_renders_into_post_tool_use) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_reaches_the_fallback_pin_and_its_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_reaches_the_fallback_pin_and_its_checksums) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_orchestrator_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_orchestrator_kind_fails) ... ok
test_unknown_worker_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_kind_defaults_to_codex (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ERROR
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ERROR
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ERROR
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/validate-agent-assets-test-rfm1bcjb/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_current_only_key_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_only_key_is_preserved) ... ok
test_current_session_start_order_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
Order is preserved; a stale bare herdr-agents command still migrates. ... ok
test_desired_current_output_is_byte_identical (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_desired_current_output_is_byte_identical) ... ok
test_empty_stdin_outputs_managed (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_empty_stdin_outputs_managed) ... ok
test_enabled_plugins_are_preserved_from_current (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_enabled_plugins_are_preserved_from_current) ... ok
test_invalid_json_outputs_managed (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_invalid_json_outputs_managed) ... ok
test_managed_hook_object_key_order_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_hook_object_key_order_is_preserved) ... ok
test_managed_permgate_replaces_stale_current_ccgate_hook (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_permgate_replaces_stale_current_ccgate_hook) ... ok
test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path) ... ok
test_managed_post_tool_use_replaces_stale_format_only_entry (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_post_tool_use_replaces_stale_format_only_entry) ... ok
test_managed_session_start_replacement_keeps_hook_order (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
Replacing a managed entry must not reorder SessionStart. ... ok
test_managed_session_start_replaces_stale_hard_coded_home_hook (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
Upgrade path: a machine that received the old hard-coded managed hook. ... ok
test_managed_wins_for_managed_key (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_wins_for_managed_key) ... ok
test_merge_is_idempotent (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_merge_is_idempotent) ... ok
test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) ... ok
test_permission_merge_preserves_custom_hook_in_mixed_entry (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_custom_hook_in_mixed_entry) ... ok
test_permission_merge_preserves_unrelated_current_hooks (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_unrelated_current_hooks) ... ok
test_real_template_preserves_herdr_matcher_and_converges (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_template_preserves_herdr_matcher_and_converges) ... ok
test_real_value_change_is_redumped (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_value_change_is_redumped) ... ok
test_reordered_but_equal_current_is_byte_identical (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_reordered_but_equal_current_is_byte_identical) ... ok
test_runtime_enabled_plugins_survive_a_managed_file_without_the_key (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_runtime_enabled_plugins_survive_a_managed_file_without_the_key) ... ok
test_trailing_newline (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_ci_smokes_statusline_tools_with_network_denied (tests.unit.test_statusline_tools.StatuslineToolsTest.test_ci_smokes_statusline_tools_with_network_denied) ... ok
test_direct_commands_use_offline_path_binaries (tests.unit.test_statusline_tools.StatuslineToolsTest.test_direct_commands_use_offline_path_binaries) ... ok
test_generated_commands_are_direct_and_static (tests.unit.test_statusline_tools.StatuslineToolsTest.test_generated_commands_are_direct_and_static) ... ok
test_mise_config_declares_the_statusline_tools_behind_the_cooldown (tests.unit.test_statusline_tools.StatuslineToolsTest.test_mise_config_declares_the_statusline_tools_behind_the_cooldown) ... ok
test_missing_binary_fails_immediately (tests.unit.test_statusline_tools.StatuslineToolsTest.test_missing_binary_fails_immediately) ... ok

======================================================================
ERROR: test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1005, in test_hook_composition_rejects_duplicate_command
    self.update_json_hook_source(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        "home/.chezmoitemplates/claude-settings-managed.json",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        "Stop",
        ^^^^^^^
        [{"hooks": [duplicate, duplicate]}],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 334, in update_json_hook_source
    data = json.loads(path.read_text())
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/__init__.py", line 371, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 358, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 374, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 67 column 15 (char 1905)

======================================================================
ERROR: test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1036, in test_hook_composition_rejects_sync_timeout_over_budget
    self.update_json_hook_source(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        "home/.chezmoitemplates/claude-settings-managed.json",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<8 lines>...
        ],
        ^^
    )
    ^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 334, in update_json_hook_source
    data = json.loads(path.read_text())
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/__init__.py", line 371, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 358, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 374, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 67 column 15 (char 1905)

======================================================================
ERROR: test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1015, in test_hook_composition_requires_permgate_first
    self.update_json_hook_source(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        "home/.chezmoitemplates/claude-settings-managed.json",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<12 lines>...
        ],
        ^^
    )
    ^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 334, in update_json_hook_source
    data = json.loads(path.read_text())
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/__init__.py", line 371, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 358, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/json/decoder.py", line 374, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 67 column 15 (char 1905)

----------------------------------------------------------------------
Ran 206 tests in 13.870s

FAILED (errors=3)
(exit 1)
```

## connected-tests-fixture-adapted

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets tests.unit.test_claude_settings_merge tests.unit.test_statusline_tools -v
test_a_declare_r_assignment_must_appear_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_command_hooks_render_after_permission_request_in_manifest_order (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_command_hooks_render_after_permission_request_in_manifest_order) ... ok
test_codex_config_renders_permgate_permission_request (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_empty_or_missing_codex_command_hooks_render_no_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_empty_or_missing_codex_command_hooks_render_no_table) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_hook_trust_hash_reproduces_codex_current_hashes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_hook_trust_hash_reproduces_codex_current_hashes) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb) ... ok
test_managed_codex_path_includes_installed_common_bin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_orchestrator_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_orchestrator_kind) ... ok
test_model_profiles_env_renders_worker_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_env_selects_no_github_store (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_selects_no_github_store) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_orchestrator_kind_defaults_to_claude (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_orchestrator_kind_defaults_to_claude) ... ok
test_plugin_versions_order_build_metadata_like_the_semver_crate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_plugin_versions_order_build_metadata_like_the_semver_crate) ... ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_handle_table_headers_with_trailing_comments (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_handle_table_headers_with_trailing_comments) ... ok
test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin) ... ok
test_profile_modify_scripts_hash_the_plugin_version_codex_loads (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_the_plugin_version_codex_loads) ... ok
test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings) ... ok
test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_replace_a_single_quoted_declared_entry (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_a_single_quoted_declared_entry) ... ok
test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root) ... ok
test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared) ... ok
test_profile_modify_scripts_replace_inline_table_and_dotted_forms (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_inline_table_and_dotted_forms) ... ok
test_profile_modify_scripts_seed_base_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_project_map_reload_hook_accepts_only_cdp_target_ids (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_accepts_only_cdp_target_ids) ... ok
test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) ... ok
test_project_map_reload_hook_guards_against_a_tab_navigating_away (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_guards_against_a_tab_navigating_away) ... ok
test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) ... ok
test_project_map_reload_hook_pins_the_bound_tab_when_it_closes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_pins_the_bound_tab_when_it_closes) ... ok
test_project_map_reload_hook_renders_into_post_tool_use (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_renders_into_post_tool_use) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_reaches_the_fallback_pin_and_its_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_reaches_the_fallback_pin_and_its_checksums) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_orchestrator_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_orchestrator_kind_fails) ... ok
test_unknown_worker_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_kind_defaults_to_codex (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/validate-agent-assets-test-mwskvogd/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_current_only_key_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_only_key_is_preserved) ... ok
test_current_session_start_order_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
Order is preserved; a stale bare herdr-agents command still migrates. ... ok
test_desired_current_output_is_byte_identical (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_desired_current_output_is_byte_identical) ... ok
test_empty_stdin_outputs_managed (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_empty_stdin_outputs_managed) ... ok
test_enabled_plugins_are_preserved_from_current (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_enabled_plugins_are_preserved_from_current) ... ok
test_invalid_json_outputs_managed (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_invalid_json_outputs_managed) ... ok
test_managed_hook_object_key_order_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_hook_object_key_order_is_preserved) ... ok
test_managed_permgate_replaces_stale_current_ccgate_hook (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_permgate_replaces_stale_current_ccgate_hook) ... ok
test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path) ... ok
test_managed_post_tool_use_replaces_stale_format_only_entry (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_post_tool_use_replaces_stale_format_only_entry) ... ok
test_managed_session_start_replacement_keeps_hook_order (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
Replacing a managed entry must not reorder SessionStart. ... ok
test_managed_session_start_replaces_stale_hard_coded_home_hook (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
Upgrade path: a machine that received the old hard-coded managed hook. ... ok
test_managed_wins_for_managed_key (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_wins_for_managed_key) ... ok
test_merge_is_idempotent (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_merge_is_idempotent) ... ok
test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) ... ok
test_permission_merge_preserves_custom_hook_in_mixed_entry (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_custom_hook_in_mixed_entry) ... ok
test_permission_merge_preserves_unrelated_current_hooks (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_unrelated_current_hooks) ... ok
test_real_template_preserves_herdr_matcher_and_converges (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_template_preserves_herdr_matcher_and_converges) ... ok
test_real_value_change_is_redumped (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_value_change_is_redumped) ... ok
test_reordered_but_equal_current_is_byte_identical (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_reordered_but_equal_current_is_byte_identical) ... ok
test_runtime_enabled_plugins_survive_a_managed_file_without_the_key (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_runtime_enabled_plugins_survive_a_managed_file_without_the_key) ... ok
test_trailing_newline (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_ci_smokes_statusline_tools_with_network_denied (tests.unit.test_statusline_tools.StatuslineToolsTest.test_ci_smokes_statusline_tools_with_network_denied) ... ok
test_direct_commands_use_offline_path_binaries (tests.unit.test_statusline_tools.StatuslineToolsTest.test_direct_commands_use_offline_path_binaries) ... ok
test_generated_commands_are_direct_and_static (tests.unit.test_statusline_tools.StatuslineToolsTest.test_generated_commands_are_direct_and_static) ... ok
test_mise_config_declares_the_statusline_tools_behind_the_cooldown (tests.unit.test_statusline_tools.StatuslineToolsTest.test_mise_config_declares_the_statusline_tools_behind_the_cooldown) ... ok
test_missing_binary_fails_immediately (tests.unit.test_statusline_tools.StatuslineToolsTest.test_missing_binary_fails_immediately) ... ok

----------------------------------------------------------------------
Ran 206 tests in 11.256s

OK
(exit 0)
```

## render-check

```text
$ make render-check
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
(exit 0)
```

## ruff

```text
$ uv run --offline --no-project --with ruff ruff check scripts/generate-agent-configs.py scripts/validate-agent-assets.py tests/unit/test_generate_agent_configs.py tests/unit/test_validate_agent_assets.py tests/unit/test_claude_settings_merge.py tests/unit/test_statusline_tools.py
B020 Loop control variable `index` overrides iterable it iterates
   --> scripts/generate-agent-configs.py:200:13
    |
198 |         indent = " " * (4 + 2 * depth)
199 |         key = f"{indent}{part}:"
200 |         for index in range(index + 1, len(lines)):
    |             ^^^^^
201 |             line = lines[index]
202 |             if line.strip() and len(line) - len(line.lstrip(" ")) < len(indent):
    |

FURB167 [*] Use of regular expression alias `re.M`
   --> scripts/generate-agent-configs.py:232:107
    |
230 |                 text = path.read_text()
231 |             for constant, field in entry["constants"].items():
232 |                 pattern = re.compile(rf'^((?:readonly |declare -r )?{re.escape(constant)}=)"[^"$`\\]*"$', re.M)
    |                                                                                                           ^^^^
233 |                 value = asset_field(asset, field)
234 |                 if not PLAIN_PIN_VALUE.fullmatch(value):
    |
help: Replace with `re.MULTILINE`
    |
231 |             for constant, field in entry["constants"].items():
    -                 pattern = re.compile(rf'^((?:readonly |declare -r )?{re.escape(constant)}=)"[^"$`\\]*"$', re.M)
232 +                 pattern = re.compile(rf'^((?:readonly |declare -r )?{re.escape(constant)}=)"[^"$`\\]*"$', re.MULTILINE)
233 |                 value = asset_field(asset, field)
    |

B023 Function definition does not bind loop variable `value`
   --> scripts/generate-agent-configs.py:236:78
    |
234 |                 if not PLAIN_PIN_VALUE.fullmatch(value):
235 |                     fail(f"assets.{name}.{field} is not a plain pin value: {value!r}")
236 |                 text, count = pattern.subn(lambda match: f'{match.group(1)}"{value}"', text)
    |                                                                              ^^^^^
237 |                 if count != 1:
238 |                     fail(f"{entry['file']} must assign {constant} exactly once for assets.{name}")
    |

SIM102 Use a single `if` statement instead of nested `if` statements
    --> scripts/generate-agent-configs.py:1448:9
     |
1446 |       stale_profiles = stale_profile_outputs(manifest)
1447 |       for path, content in outputs.items():
1448 | /         if args.check:
1449 | |             if not path.exists() or path.read_text() != content:
     | |________________________________________________________________^
1450 |                   stale.append(path.relative_to(ROOT))
1451 |       if args.check:
     |
help: Combine `if` statements using `and`
     |
1447 |     for path, content in outputs.items():
     -         if args.check:
     -             if not path.exists() or path.read_text() != content:
     -                 stale.append(path.relative_to(ROOT))
1448 +         if args.check and (not path.exists() or path.read_text() != content):
1449 +             stale.append(path.relative_to(ROOT))
1450 |     if args.check:
     |
note: This is an unsafe fix and may change runtime behavior

EXE001 Shebang is present but file is not executable
 --> scripts/validate-agent-assets.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Validate Codex, Claude Code, MCP, plugin, and skill assets."""
  |

I001 [*] Import block is un-sorted or un-formatted
  --> scripts/validate-agent-assets.py:4:1
   |
 2 |   """Validate Codex, Claude Code, MCP, plugin, and skill assets."""
 3 |
 4 | / from __future__ import annotations
 5 | |
 6 | | import configparser
 7 | | import fnmatch
 8 | | import json
 9 | | import os
10 | | import posixpath
11 | | import re
12 | | import subprocess
13 | | import sys
14 | | from collections.abc import Iterable
15 | | from functools import cache
16 | | from pathlib import Path
17 | | from typing import Any
18 | |
19 | | import tomllib
   | |______________^
20 |
21 |   try:
   |
help: Organize imports
   |
13 | import sys
14 + import tomllib
15 | from collections.abc import Iterable
16 | from functools import cache
17 | from pathlib import Path
18 | from typing import Any
   -
   - import tomllib
19 |
   |

SIM102 Use a single `if` statement instead of nested `if` statements
   --> scripts/validate-agent-assets.py:139:9
    |
138 |           commands = [hook_command_string(hook) for hook in hooks]
139 | /         if event == "PermissionRequest" and any("permgate" in command for command in commands):
140 | |             if not commands or "permgate" not in commands[0]:
    | |_____________________________________________________________^
141 |                   findings.append(f"permgate-first source={source} event={event} first={commands[0]!r}")
    |
help: Combine `if` statements using `and`

C401 Unnecessary generator (rewrite as a set comprehension)
   --> scripts/validate-agent-assets.py:894:12
    |
892 |             fail(f"MCP server {name} must be disabled by default in the shared manifest")
893 |         agents = server.get("agents", {})
894 |         if set(agent for agent, enabled in agents.items() if enabled) != targets:
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
895 |             fail(f"MCP server {name} must be exposed to every target agent")
896 |         transport = server.get("transport")
    |
help: Rewrite as a set comprehension
    |
893 |         agents = server.get("agents", {})
    -         if set(agent for agent, enabled in agents.items() if enabled) != targets:
894 +         if {agent for agent, enabled in agents.items() if enabled} != targets:
895 |             fail(f"MCP server {name} must be exposed to every target agent")
    |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> scripts/validate-agent-assets.py:951:18
    |
949 |           if path.stat().st_mode & 0o111 == 0:
950 |               fail(f"{path} must be executable")
951 |           result = subprocess.run(
    |  __________________^
952 | |             [str(path)],
953 | |             input="",
954 | |             text=True,
955 | |             stdout=subprocess.PIPE,
956 | |             stderr=subprocess.PIPE,
957 | |             check=False,
958 | |         )
    | |_________^
959 |           if result.returncode != 0:
960 |               fail(f"{path} must run successfully: {result.stderr.strip()}")
    |
help: Replace with `capture_output` keyword argument
    |
954 |             text=True,
    -             stdout=subprocess.PIPE,
    -             stderr=subprocess.PIPE,
955 +             capture_output=True,
956 |             check=False,
    |
note: This is an unsafe fix and may change runtime behavior

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_claude_settings_merge.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Exercise Claude settings modify-script merge behavior."""
  |

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
  --> tests/unit/test_claude_settings_merge.py:37:18
   |
35 |           env["CHEZMOI_SOURCE_DIR"] = str(self.source_dir)
36 |           env["CHEZMOI_HOME_DIR"] = str(self.home_dir)
37 |           result = subprocess.run(
   |  __________________^
38 | |             ["uv", "run", "python", str(MERGE_SCRIPT)],
39 | |             input=current,
40 | |             text=True,
41 | |             stdout=subprocess.PIPE,
42 | |             stderr=subprocess.PIPE,
43 | |             env=env,
44 | |             check=True,
45 | |         )
   | |_________^
46 |           json.loads(result.stdout)
47 |           return result.stdout
   |
help: Replace with `capture_output` keyword argument
   |
40 |             text=True,
   -             stdout=subprocess.PIPE,
   -             stderr=subprocess.PIPE,
41 +             capture_output=True,
42 |             env=env,
   |
note: This is an unsafe fix and may change runtime behavior

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_generate_agent_configs.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Exercise focused checks in generate-agent-configs.py."""
  |

SIM117 Use a single `with` statement with multiple contexts instead of nested `with` statements
   --> tests/unit/test_generate_agent_configs.py:424:13
    |
422 |           )
423 |           for name, path, value in cases:
424 | /             with self.subTest(target=f"{name}.{path}", value=value):
425 | |                 with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
    | |______________________________________________________________________________________________^
426 |                       self.module.set_asset_field(self.MANIFEST_TEXT, name, path, value)
    |
help: Combine `with` statements

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:602:18
    |
600 |           self.assertTrue(standard_profile.stat().st_mode & 0o111)
601 |
602 |           result = subprocess.run(
    |  __________________^
603 | |             [str(standard_profile)],
604 | |             input='model = "runtime"\nmodel_reasoning_effort = "high"\n\n[hooks.state]\ntrusted = true\n',
605 | |             text=True,
606 | |             stdout=subprocess.PIPE,
607 | |             stderr=subprocess.PIPE,
608 | |             env={
609 | |                 **os.environ,
610 | |                 "HOME": str(self.temp_dir / "target-home"),
611 | |                 "CHEZMOI_SOURCE_DIR": str(self.temp_dir / "home"),
612 | |                 "CHEZMOI_HOME_DIR": str(self.temp_dir / "target-home"),
613 | |             },
614 | |             check=False,
615 | |         )
    | |_________^
616 |
617 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument
    |
605 |             text=True,
    -             stdout=subprocess.PIPE,
    -             stderr=subprocess.PIPE,
606 +             capture_output=True,
607 |             env={
    |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:639:18
    |
638 |           home = self.temp_dir / "target-home"
639 |           result = subprocess.run(
    |  __________________^
640 | |             [str(security_profile)],
641 | |             input="",
642 | |             text=True,
643 | |             stdout=subprocess.PIPE,
644 | |             stderr=subprocess.PIPE,
645 | |             env={**os.environ, "HOME": str(home)},
646 | |             check=False,
647 | |         )
    | |_________^
648 |
649 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument
    |
642 |             text=True,
    -             stdout=subprocess.PIPE,
    -             stderr=subprocess.PIPE,
643 +             capture_output=True,
644 |             env={**os.environ, "HOME": str(home)},
    |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:787:22
    |
785 |           def render(name: str) -> dict:
786 |               path = self.temp_dir / f"home/dot_codex/modify_private_{name}.config.toml"
787 |               result = subprocess.run(
    |  ______________________^
788 | |                 [str(path)],
789 | |                 input="",
790 | |                 text=True,
791 | |                 stdout=subprocess.PIPE,
792 | |                 stderr=subprocess.PIPE,
793 | |                 check=False,
794 | |             )
    | |_____________^
795 |               self.assertEqual(result.returncode, 0, result.stderr)
796 |               return tomllib.loads(result.stdout)
    |
help: Replace with `capture_output` keyword argument
    |
790 |                 text=True,
    -                 stdout=subprocess.PIPE,
    -                 stderr=subprocess.PIPE,
791 +                 capture_output=True,
792 |                 check=False,
    |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:835:18
    |
833 |               "trusted = true\n"
834 |           )
835 |           result = subprocess.run(
    |  __________________^
836 | |             [str(standard_profile)],
837 | |             input=current,
838 | |             text=True,
839 | |             stdout=subprocess.PIPE,
840 | |             stderr=subprocess.PIPE,
841 | |             env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
842 | |             check=False,
843 | |         )
    | |_________^
844 |
845 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument
    |
838 |             text=True,
    -             stdout=subprocess.PIPE,
    -             stderr=subprocess.PIPE,
839 +             capture_output=True,
840 |             env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
    |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   --> tests/unit/test_generate_agent_configs.py:870:18
    |
868 |               'name = "second"\n'
869 |           )
870 |           result = subprocess.run(
    |  __________________^
871 | |             [str(standard_profile)],
872 | |             input=current,
873 | |             text=True,
874 | |             stdout=subprocess.PIPE,
875 | |             stderr=subprocess.PIPE,
876 | |             env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
877 | |             check=False,
878 | |         )
    | |_________^
879 |
880 |           self.assertEqual(result.returncode, 0, result.stderr)
    |
help: Replace with `capture_output` keyword argument
    |
873 |             text=True,
    -             stdout=subprocess.PIPE,
    -             stderr=subprocess.PIPE,
874 +             capture_output=True,
875 |             env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
    |
note: This is an unsafe fix and may change runtime behavior

S102 Use of `exec` detected
   --> tests/unit/test_generate_agent_configs.py:904:9
    |
902 |     def hook_trust_namespace(self, manifest: dict) -> dict:
903 |         namespace = {"sys": sys, "Path": Path, "HOOK_TRUST": self.module.codex_hook_trust(manifest)}
904 |         exec(self.module.HOOK_TRUST_CODE, namespace)
    |         ^^^^
905 |         return namespace
    |

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
    --> tests/unit/test_generate_agent_configs.py:1254:18
     |
1252 |           )
1253 |
1254 |           result = subprocess.run(
     |  __________________^
1255 | |             [str(standard_profile)],
1256 | |             input=(
1257 | |                 "[hooks.state]\n\n"
1258 | |                 '[hooks.state."/home/.codex/config.toml:permission_request:0:0"]\n'
1259 | |                 'trusted_hash = "sha256:profile"\n'
1260 | |             ),
1261 | |             text=True,
1262 | |             stdout=subprocess.PIPE,
1263 | |             stderr=subprocess.PIPE,
1264 | |             env={**os.environ, "HOME": str(home)},
1265 | |             check=False,
1266 | |         )
     | |_________^
1267 |
1268 |           self.assertEqual(result.returncode, 0, result.stderr)
     |
help: Replace with `capture_output` keyword argument
     |
1261 |             text=True,
     -             stdout=subprocess.PIPE,
     -             stderr=subprocess.PIPE,
1262 +             capture_output=True,
1263 |             env={**os.environ, "HOME": str(home)},
     |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
    --> tests/unit/test_generate_agent_configs.py:1283:18
     |
1281 |           current = '[hooks.state."hook"]\ntrusted_hash = "sha256:profile"\n'
1282 |
1283 |           result = subprocess.run(
     |  __________________^
1284 | |             [str(profile)],
1285 | |             input=current,
1286 | |             text=True,
1287 | |             stdout=subprocess.PIPE,
1288 | |             stderr=subprocess.PIPE,
1289 | |             env={**os.environ, "HOME": str(home)},
1290 | |             check=False,
1291 | |         )
     | |_________^
1292 |
1293 |           self.assertEqual(result.returncode, 0, result.stderr)
     |
help: Replace with `capture_output` keyword argument
     |
1286 |             text=True,
     -             stdout=subprocess.PIPE,
     -             stderr=subprocess.PIPE,
1287 +             capture_output=True,
1288 |             env={**os.environ, "HOME": str(home)},
     |
note: This is an unsafe fix and may change runtime behavior

UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
    --> tests/unit/test_generate_agent_configs.py:1310:18
     |
1308 |           current = '[hooks.state."hook"]\ntrusted_hash = "sha256:same"\n'
1309 |
1310 |           result = subprocess.run(
     |  __________________^
1311 | |             [str(profile)],
1312 | |             input=current,
1313 | |             text=True,
1314 | |             stdout=subprocess.PIPE,
1315 | |             stderr=subprocess.PIPE,
1316 | |             env={**os.environ, "HOME": str(home)},
1317 | |             check=False,
1318 | |         )
     | |_________^
1319 |
1320 |           self.assertEqual(result.returncode, 0, result.stderr)
     |
help: Replace with `capture_output` keyword argument
     |
1313 |             text=True,
     -             stdout=subprocess.PIPE,
     -             stderr=subprocess.PIPE,
1314 +             capture_output=True,
1315 |             env={**os.environ, "HOME": str(home)},
     |
note: This is an unsafe fix and may change runtime behavior

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_statusline_tools.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Verify statusline tools are declared in mise and execute without network installers."""
  |

I001 [*] Import block is un-sorted or un-formatted
  --> tests/unit/test_statusline_tools.py:4:1
   |
 2 |   """Verify statusline tools are declared in mise and execute without network installers."""
 3 |
 4 | / from __future__ import annotations
 5 | |
 6 | | import json
 7 | | import os
 8 | | import runpy
 9 | | import subprocess
10 | | import tempfile
11 | | import time
12 | | import tomllib
13 | | import unittest
14 | | from pathlib import Path
   | |________________________^
help: Organize imports
   |
15 |
   -
16 | ROOT = Path(__file__).resolve().parents[2]
   |

PLW1510 `subprocess.run` without explicit `check` argument
  --> tests/unit/test_statusline_tools.py:74:22
   |
72 |         for command in self.commands():
73 |             started = time.monotonic()
74 |             result = subprocess.run(
   |                      ^^^^^^^^^^^^^^
75 |                 command,
76 |                 shell=True,
   |
help: Add explicit `check=False`
   |
75 |                 command,
   -                 shell=True,
76 +                 check=False, shell=True,
77 |                 executable="/bin/sh",
   |
note: This suggestion may be incorrect or produce invalid syntax. It requires manual review and cannot be applied automatically

EXE001 Shebang is present but file is not executable
 --> tests/unit/test_validate_agent_assets.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Exercise focused checks in validate-agent-assets.py."""
  |

FLY002 Consider f-string instead of string join
   --> tests/unit/test_validate_agent_assets.py:253:13
    |
251 |       def write_codex_config(self, sandbox_workspace_write: str, projects_toml: str = "") -> None:
252 |           (self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml").write_text(
253 | /             "\n".join(
254 | |                 [
255 | |                     "#:schema https://developers.openai.com/codex/config-schema.json",
256 | |                     'model = "gpt-5.5"',
257 | |                     'model_reasoning_effort = "high"',
258 | |                     'sandbox_mode = "workspace-write"',
259 | |                     "",
260 | |                     "[sandbox_workspace_write]",
261 | |                     sandbox_workspace_write,
262 | |                     "",
263 | |                     "[features]",
264 | |                     "plugins = true",
265 | |                     "hooks = true",
266 | |                     "plugin_hooks = true",
267 | |                     "",
268 | |                     "[shell_environment_policy]",
269 | |                     'inherit = "core"',
270 | |                     'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
271 | |                     "",
272 | |                     projects_toml,
273 | |                 ]
274 | |             )
    | |_____________^
275 |           )
    |
help: Replace with f-string
    |
252 |         (self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml").write_text(
    -             "\n".join(
    -                 [
    -                     "#:schema https://developers.openai.com/codex/config-schema.json",
    -                     'model = "gpt-5.5"',
    -                     'model_reasoning_effort = "high"',
    -                     'sandbox_mode = "workspace-write"',
    -                     "",
    -                     "[sandbox_workspace_write]",
    -                     sandbox_workspace_write,
    -                     "",
    -                     "[features]",
    -                     "plugins = true",
    -                     "hooks = true",
    -                     "plugin_hooks = true",
    -                     "",
    -                     "[shell_environment_policy]",
    -                     'inherit = "core"',
    -                     'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
    -                     "",
    -                     projects_toml,
    -                 ]
    -             )
253 +             f'#:schema https://developers.openai.com/codex/config-schema.json\nmodel = "gpt-5.5"\nmodel_reasoning_effort = "high"\nsandbox_mode = "workspace-write"\n\n[sandbox_workspace_write]\n{sandbox_workspace_write}\n\n[features]\nplugins = true\nhooks = true\nplugin_hooks = true\n\n[shell_environment_policy]\ninherit = "core"\nset = {{ PATH = "{{{{ .chezmoi.homeDir }}}}/.local/bin:/usr/bin:/bin" }}\n\n{projects_toml}'
254 |         )
    |
note: This is an unsafe fix and may change runtime behavior

UP037 [*] Remove quotes from type annotation
    --> tests/unit/test_validate_agent_assets.py:1624:41
     |
1622 |         shutil.rmtree(self.temp_dir)
1623 |
1624 |     def run_mask(self, *paths: Path) -> "subprocess.CompletedProcess[str]":
     |                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1625 |         return subprocess.run(
1626 |             [sys.executable, str(VALIDATOR), "--mask-secrets", *map(str, paths)],
     |
help: Remove quotes
     |
1623 |
     -     def run_mask(self, *paths: Path) -> "subprocess.CompletedProcess[str]":
1624 +     def run_mask(self, *paths: Path) -> subprocess.CompletedProcess[str]:
1625 |         return subprocess.run(
     |

Found 28 errors.
[*] 4 fixable with `--fix` (13 unsafe fixes available with `--fix --unsafe-fixes`).
(exit 1)
```

## Ruff baseline comparison

```text
$ uv run --offline --no-project /tmp/codex-T130-ruff-compare.py
{
  "baseline_diagnostics": 28,
  "current_diagnostics": 28,
  "introduced": [],
  "removed": []
}
```

## Amendment2

Full task read and byte-identical copy verified: SHA256 3cbe38cbb773e9f2c9c1c7619aa704e6f07d05e5bdd5ee7c02288f2a11735dd4. Narrow env key merge plus its newly named regression authorized before source edits.

## env-preservation-red

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win -v
test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win) ... FAIL

======================================================================
FAIL: test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_claude_settings_merge.py", line 88, in test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win
    self.assertEqual(existing | managed["env"], json.loads(once)["env"])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: {'CUSTOM_RUNTIME_MARKER': 'keep-me', 'ANTHR[188 chars]rue'} != {'GH_TELEMETRY': 'false', 'DO_NOT_TRACK': '[62 chars]rue'}
- {'ANTHROPIC_BASE_URL': 'https://provider.invalid',
-  'AWS_EC2_METADATA_DISABLED': 'true',
? ^

+ {'AWS_EC2_METADATA_DISABLED': 'true',
? ^

   'CHECKPOINT_DISABLE': '1',
-  'CUSTOM_RUNTIME_MARKER': 'keep-me',
   'DO_NOT_TRACK': '1',
-  'GH_TELEMETRY': 'false',
?                         ^

+  'GH_TELEMETRY': 'false'}
?                         ^

-  'HTTPS_PROXY': 'https://proxy.invalid'}

----------------------------------------------------------------------
Ran 1 test in 0.094s

FAILED (failures=1)
(exit 1)
```

## env-test-format

```text
$ uv run --offline --no-project --with ruff ruff format tests/unit/test_claude_settings_merge.py
1 file reformatted
(exit 0)
```

## final-connected-tests

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets tests.unit.test_claude_settings_merge tests.unit.test_statusline_tools -v
test_a_declare_r_assignment_must_appear_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_command_hooks_render_after_permission_request_in_manifest_order (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_command_hooks_render_after_permission_request_in_manifest_order) ... ok
test_codex_config_renders_permgate_permission_request (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_empty_or_missing_codex_command_hooks_render_no_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_empty_or_missing_codex_command_hooks_render_no_table) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_hook_trust_hash_reproduces_codex_current_hashes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_hook_trust_hash_reproduces_codex_current_hashes) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb) ... ok
test_managed_codex_path_includes_installed_common_bin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_orchestrator_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_orchestrator_kind) ... ok
test_model_profiles_env_renders_worker_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_env_selects_no_github_store (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_selects_no_github_store) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_orchestrator_kind_defaults_to_claude (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_orchestrator_kind_defaults_to_claude) ... ok
test_plugin_versions_order_build_metadata_like_the_semver_crate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_plugin_versions_order_build_metadata_like_the_semver_crate) ... ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_handle_table_headers_with_trailing_comments (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_handle_table_headers_with_trailing_comments) ... ok
test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin) ... ok
test_profile_modify_scripts_hash_the_plugin_version_codex_loads (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_the_plugin_version_codex_loads) ... ok
test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings) ... ok
test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_replace_a_single_quoted_declared_entry (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_a_single_quoted_declared_entry) ... ok
test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root) ... ok
test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared) ... ok
test_profile_modify_scripts_replace_inline_table_and_dotted_forms (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_inline_table_and_dotted_forms) ... ok
test_profile_modify_scripts_seed_base_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_project_map_reload_hook_accepts_only_cdp_target_ids (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_accepts_only_cdp_target_ids) ... ok
test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) ... ok
test_project_map_reload_hook_guards_against_a_tab_navigating_away (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_guards_against_a_tab_navigating_away) ... ok
test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) ... ok
test_project_map_reload_hook_pins_the_bound_tab_when_it_closes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_pins_the_bound_tab_when_it_closes) ... ok
test_project_map_reload_hook_renders_into_post_tool_use (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_renders_into_post_tool_use) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_reaches_the_fallback_pin_and_its_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_reaches_the_fallback_pin_and_its_checksums) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_orchestrator_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_orchestrator_kind_fails) ... ok
test_unknown_worker_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_kind_defaults_to_codex (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/validate-agent-assets-test-__gxvtwc/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_current_only_key_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_only_key_is_preserved) ... ok
test_current_session_start_order_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
Order is preserved; a stale bare herdr-agents command still migrates. ... ok
test_desired_current_output_is_byte_identical (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_desired_current_output_is_byte_identical) ... ok
test_empty_stdin_outputs_managed (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_empty_stdin_outputs_managed) ... ok
test_enabled_plugins_are_preserved_from_current (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_enabled_plugins_are_preserved_from_current) ... ok
test_invalid_json_outputs_managed (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_invalid_json_outputs_managed) ... ok
test_managed_hook_object_key_order_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_hook_object_key_order_is_preserved) ... ok
test_managed_permgate_replaces_stale_current_ccgate_hook (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_permgate_replaces_stale_current_ccgate_hook) ... ok
test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path) ... ok
test_managed_post_tool_use_replaces_stale_format_only_entry (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_post_tool_use_replaces_stale_format_only_entry) ... ok
test_managed_session_start_replacement_keeps_hook_order (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
Replacing a managed entry must not reorder SessionStart. ... ok
test_managed_session_start_replaces_stale_hard_coded_home_hook (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
Upgrade path: a machine that received the old hard-coded managed hook. ... ok
test_managed_wins_for_managed_key (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_wins_for_managed_key) ... ok
test_merge_is_idempotent (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_merge_is_idempotent) ... ok
test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win) ... ok
test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) ... ok
test_permission_merge_preserves_custom_hook_in_mixed_entry (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_custom_hook_in_mixed_entry) ... ok
test_permission_merge_preserves_unrelated_current_hooks (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_unrelated_current_hooks) ... ok
test_real_template_preserves_herdr_matcher_and_converges (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_template_preserves_herdr_matcher_and_converges) ... ok
test_real_value_change_is_redumped (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_value_change_is_redumped) ... ok
test_reordered_but_equal_current_is_byte_identical (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_reordered_but_equal_current_is_byte_identical) ... ok
test_runtime_enabled_plugins_survive_a_managed_file_without_the_key (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_runtime_enabled_plugins_survive_a_managed_file_without_the_key) ... ok
test_trailing_newline (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_ci_smokes_statusline_tools_with_network_denied (tests.unit.test_statusline_tools.StatuslineToolsTest.test_ci_smokes_statusline_tools_with_network_denied) ... ok
test_direct_commands_use_offline_path_binaries (tests.unit.test_statusline_tools.StatuslineToolsTest.test_direct_commands_use_offline_path_binaries) ... ok
test_generated_commands_are_direct_and_static (tests.unit.test_statusline_tools.StatuslineToolsTest.test_generated_commands_are_direct_and_static) ... ok
test_mise_config_declares_the_statusline_tools_behind_the_cooldown (tests.unit.test_statusline_tools.StatuslineToolsTest.test_mise_config_declares_the_statusline_tools_behind_the_cooldown) ... ok
test_missing_binary_fails_immediately (tests.unit.test_statusline_tools.StatuslineToolsTest.test_missing_binary_fails_immediately) ... ok

----------------------------------------------------------------------
Ran 207 tests in 12.734s

OK
(exit 0)
```

## source-integrity

```text
$ uv run --offline --no-project --with pyyaml /tmp/codex-T130-integrity.py
{
  "baseline": "ce032e14830b125f677a83c383986e02084bb597",
  "task_sha256": "3cbe38cbb773e9f2c9c1c7619aa704e6f07d05e5bdd5ee7c02288f2a11735dd4",
  "source_sha256": {
    "home/.chezmoitemplates/claude-settings-managed.json": "55a6acc5d1a42a510f4ca0419fbfc7cf545d665d67d806e19cd300e2b186404e",
    "home/dot_agents/agent-config.yaml": "611b67e5262c3e0df2480a91627b2b561b7267f22915b40d71a71ef22c7f71d6",
    "home/dot_claude/modify_private_settings.json": "e39ebb0e1b9021900a1f2cf4eab2307ad71b640a349e030db0273845e9479215",
    "home/dot_mise/config.toml": "effd12cca398c4252d4cd21efebd4bf147add970ae27b413af55e1ecad297d2c",
    "scripts/generate-agent-configs.py": "80d4be814b226fc251dc7788a17b80477d93cf597b07be3e4e66da36a6eb69cf",
    "scripts/validate-agent-assets.py": "669046641fed18c32ca0a15216535f856ab1cc45e0cdadf79306ae30e4ef584c",
    "tests/unit/test_claude_settings_merge.py": "76ead16113adc63df0001fadfa34a1415782196c9fbd3552fde0f5f377fee3fb",
    "tests/unit/test_generate_agent_configs.py": "e06316a72bc26e8f0cf5f92374cc331686f8a92c77da013b13af06afb168bd3b",
    "tests/unit/test_statusline_tools.py": "48ff74af47ad88ddff5bb22be8a9c43d16862d7a29e7f7a20f57ab0ffe36ff9f",
    "tests/unit/test_validate_agent_assets.py": "7c201a7060a3a7c21ea50df1247d9f08797ce2580851d7f7278bfbbfe4545cea"
  },
  "source_changed": 140,
  "test_added": 242,
  "generated_changed_excluded": 144,
  "unrelated_manifest_and_Codex_defaults_unchanged": true,
  "existing_deny_and_sandbox_flags_and_unix_socket_list_unchanged": true,
  "mise_only_blcc_fixed_pin": true,
  "numstat": "115\t29\thome/.chezmoitemplates/claude-settings-managed.json\n56\t10\thome/dot_agents/agent-config.yaml\n10\t0\thome/dot_claude/modify_private_settings.json\n1\t1\thome/dot_mise/config.toml\n17\t8\tscripts/generate-agent-configs.py\n32\t5\tscripts/validate-agent-assets.py\n70\t1\ttests/unit/test_claude_settings_merge.py\n115\t3\ttests/unit/test_generate_agent_configs.py\n3\t1\ttests/unit/test_statusline_tools.py\n54\t1\ttests/unit/test_validate_agent_assets.py\n"
}
(exit 0)
```

## Ruff baseline comparison

```text
$ uv run --offline --no-project /tmp/codex-T130-ruff-compare.py
{
  "baseline_diagnostics": 28,
  "current_diagnostics": 28,
  "introduced": [],
  "removed": []
}
```

## final-format-check

```text
$ uv run --offline --no-project --with ruff ruff format --check scripts/generate-agent-configs.py scripts/validate-agent-assets.py tests/unit/test_generate_agent_configs.py tests/unit/test_validate_agent_assets.py tests/unit/test_claude_settings_merge.py tests/unit/test_statusline_tools.py
6 files already formatted
(exit 0)
```

## independent-review-initial.md

# T130 independent security source review — Amendment 1

Review scope: ten named working-tree source/test files on feat/claude-sandbox-integration against baseline ce032e14830b125f677a83c383986e02084bb597. This is worker source-phase evidence, not final-head audit, CI approval, or orchestrator acceptance. Repository files were read only; artifacts were written under /tmp. No package install, network installer, local Bats, live apply/restart, GitHub mutation, or Crit UI was run. Official documentation was read using the web tool. Crit data was unavailable per the parent's status evidence; this is the authorized independent fallback.

Plan/todo (owner: independent reviewer): read dispatched task and all named diffs plus connected modifier/validator/test callers; independently run three required tests; reproduce any concrete failure; bind current hashes and report. All complete. One finding remains open. Scope includes the parent's final one-line validator fixture adaptation, not any subsequently proposed env merge.

## Finding

**P2 — high confidence — scripts/generate-agent-configs.py:436: Preserve existing unrelated env keys when introducing managed env.** Adding the new top-level env map makes the existing modifier's merge_settings replace the entire current env dictionary (home/dot_claude/modify_private_settings.json:171–180), rather than only the four newly managed entries. On the next chezmoi apply an existing ANTHROPIC_BASE_URL, proxy configuration, or other runtime env settings disappear. The new real modifier test preserves runtimeOnly and enabledPlugins but never supplies an existing env object, so it misses this regression. I ran the actual modifier entry point with an isolated source/home for both Darwin and Linux: baseline preserves both supplied env keys, while the candidate silently discards both and emits only the four new managed values. No real credentials were used. Preserve unknown current env entries, let managed entries override collisions, and test both OS paths plus a second application. The current task limits modifier changes to conditional rendering, so the parent correctly sought an amendment before implementing that fix.

This is introduced by the new generated env map, not a request to broaden the old merger for arbitrary settings. The failure is material configuration loss even though the resulting JSON is valid and repeated application is stable. No approval is granted for this snapshot.

## Other review conclusions

- Read the complete dispatched Amendment 1 task; its SHA matches the requested value below. Threat-table entries cover the named paths and controls. Current source stays within the ten-path scope and the 200 production/1000 test-addition caps (138 production changed lines; 215 test additions).
- Manifest keeps existing deny rules and Codex writable roots unchanged. New write roots are named and OS-specific; macOS alone receives Library/Caches/mise. The generated macOS exclusions contain agmsg-dispatch only; Linux adds gh and the rendered absolute seat-claim script. No sysmond exemption or allowAllUnixSockets widening is introduced.
- Network additions are only pypi.org and files.pythonhosted.org. Mach access is limited to com.apple.trustd.agent on Darwin and omitted on Linux. Validator rejects forbidden telemetry/metadata hosts, including datadoghq.com subdomains, unapproved Mach services, allowAllUnixSockets true, and macOS gh exclusion. The Linux-only template-corruption subcase proves both renderings are validated.
- Official sandboxing documentation (https://code.claude.com/docs/en/sandboxing) explicitly lists network.allowMachLookup. Its exclusion section states that an unstarred pattern is exact and a trailing space-star includes arguments; matching is against command text, so the absolute rendered script pattern is justified. The document also explains content-specific ask rules still apply to sandboxed commands. These are documentation-derived checks, not live sandbox proof. The parent records the blocc lookup as v0.6.0; the mise diff changes only latest to 0.6.0.
- gh write-operation ask prefixes include separate/joined short and long method variants and field options. They do not provide complete authorization against flags following the API path; the manifest explicitly records this task-authorized shortcut. The integration gate remains the stated authority. No claim of comprehensive gh write prevention is made.
- Renderer emits one Darwin/Linux conditional, and the validator/modifier resolve that exact conditional before JSON parsing. The modifier uses host platform and existing sourceDir/homeDir substitution. It introduces no eval, command execution of manifest content, secrets, or new path authority. Existing path substitution semantics remain unchanged.
- The real modifier regression test runs subprocess entry points on both OS values with temporary source/home paths and verifies idempotence and runtime keys. Its missing env case is the finding above. Statusline fixtures now resolve the conditional via the modifier helper, retaining their assertions. Connected herdr test uses its own simple JSON baseline and is unaffected.
- Reviewed update_json_hook_source adaptation at tests/unit/test_validate_agent_assets.py:334: rendering before json.loads is necessary after introducing the conditional; existing hook assertions remain. The parent's first connected-suite run exposed three parse errors here and was not misrepresented as a pass. I do not claim the rerun or full validator passed; those are parent-owned pending evidence at this review snapshot.
- The source report.md and sandbox.md were not yet present during this source-phase review. validation.md contains historical task SHA followed by amendment evidence and in-progress check output; these drafts must be completed before final acceptance. No final CI or Bot acceptance claim was reviewed or endorsed.

## Independent checks and commands

Read full task with:
`cat .orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md`
Read the ten-file diff with `git diff ce032e14830b125f677a83c383986e02084bb597 -- <ten named paths>`; exact diff snapshot is saved as /tmp/codex-T130-security-diff.patch. Read connected merge_settings/main/render helpers, validator hook rendering, statusline helpers, generator tests, and matching references found via `rg -n 'claude-settings-managed.json|json.loads\(path.read_text\(' scripts tests/unit home/dot_claude/modify_private_settings.json`. Consulted graph summaries first; graph revision 940a3a2b differs from current baseline and is stale for the affected code; source reads are authoritative.

Required independent test command (with PYTHONDONTWRITEBYTECODE to avoid source bytecode writes):
```sh
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging -v
```
First run: three tests passed in 0.415s. Repeated after the one-line validator fixture adaptation: three tests passed in 0.251s. Full final output:
```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.251s

OK
```

Actual modifier reproduction used this command inside a Python harness for both baseline and candidate and each host value:
```python
command = [sys.executable, "-c", 'import platform,runpy,sys; platform.system=lambda:sys.argv[1]; runpy.run_path(sys.argv[2],run_name="__main__")', host, str(src / "modifier.py")]
result = subprocess.run(command, input=json.dumps(current), text=True, capture_output=True, env=env)
result.check_returncode()
```
The harness used tempfile.TemporaryDirectory(dir="/tmp"), copied the two baseline files with `git show ce032e14830b125f677a83c383986e02084bb597:<path>` and the candidate files with Path.read_bytes(), and set CHEZMOI_SOURCE_DIR, CHEZMOI_HOME_DIR and PYTHONDONTWRITEBYTECODE=1 to the fixture. It supplied only dummy nonsecret env values and runtimeOnly. Full output:
```text
{"revision": "baseline", "host": "Darwin", "exit_code": 0, "input_env": {"CUSTOM_RUNTIME_MARKER": "keep-me", "ANTHROPIC_BASE_URL": "https://example.invalid"}, "output_env": {"CUSTOM_RUNTIME_MARKER": "keep-me", "ANTHROPIC_BASE_URL": "https://example.invalid"}, "preserved": true, "runtimeOnly": {"keep": true}}
{"revision": "baseline", "host": "Linux", "exit_code": 0, "input_env": {"CUSTOM_RUNTIME_MARKER": "keep-me", "ANTHROPIC_BASE_URL": "https://example.invalid"}, "output_env": {"CUSTOM_RUNTIME_MARKER": "keep-me", "ANTHROPIC_BASE_URL": "https://example.invalid"}, "preserved": true, "runtimeOnly": {"keep": true}}
{"revision": "candidate", "host": "Darwin", "exit_code": 0, "input_env": {"CUSTOM_RUNTIME_MARKER": "keep-me", "ANTHROPIC_BASE_URL": "https://example.invalid"}, "output_env": {"GH_TELEMETRY": "false", "DO_NOT_TRACK": "1", "CHECKPOINT_DISABLE": "1", "AWS_EC2_METADATA_DISABLED": "true"}, "preserved": false, "runtimeOnly": {"keep": true}}
{"revision": "candidate", "host": "Linux", "exit_code": 0, "input_env": {"CUSTOM_RUNTIME_MARKER": "keep-me", "ANTHROPIC_BASE_URL": "https://example.invalid"}, "output_env": {"GH_TELEMETRY": "false", "DO_NOT_TRACK": "1", "CHECKPOINT_DISABLE": "1", "AWS_EC2_METADATA_DISABLED": "true"}, "preserved": false, "runtimeOnly": {"keep": true}}
```

Caps command: `git diff --numstat ce032e14830b125f677a83c383986e02084bb597 -- <ten named paths>`. Counts sum additions+deletions outside tests, excluding generated template; test cap counts additions. Output:
```text
115	29	home/.chezmoitemplates/claude-settings-managed.json
56	10	home/dot_agents/agent-config.yaml
8	0	home/dot_claude/modify_private_settings.json
1	1	home/dot_mise/config.toml
17	8	scripts/generate-agent-configs.py
32	5	scripts/validate-agent-assets.py
43	1	tests/unit/test_claude_settings_merge.py
115	3	tests/unit/test_generate_agent_configs.py
3	1	tests/unit/test_statusline_tools.py
54	1	tests/unit/test_validate_agent_assets.py
production_changed=138; test_added=215
```

Task/source hash command: Python hashlib.sha256(Path(path).read_bytes()).hexdigest() for task plus ten source paths. Current snapshot:
```json
{
  ".orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md": "525e493b2aa2cdd7a0a426302cd446bcbdc13f5cb6fc9537aeae86be236cf1c8",
  "home/dot_agents/agent-config.yaml": "611b67e5262c3e0df2480a91627b2b561b7267f22915b40d71a71ef22c7f71d6",
  "scripts/generate-agent-configs.py": "80d4be814b226fc251dc7788a17b80477d93cf597b07be3e4e66da36a6eb69cf",
  "scripts/validate-agent-assets.py": "669046641fed18c32ca0a15216535f856ab1cc45e0cdadf79306ae30e4ef584c",
  "home/.chezmoitemplates/claude-settings-managed.json": "55a6acc5d1a42a510f4ca0419fbfc7cf545d665d67d806e19cd300e2b186404e",
  "home/dot_mise/config.toml": "effd12cca398c4252d4cd21efebd4bf147add970ae27b413af55e1ecad297d2c",
  "tests/unit/test_generate_agent_configs.py": "e06316a72bc26e8f0cf5f92374cc331686f8a92c77da013b13af06afb168bd3b",
  "tests/unit/test_validate_agent_assets.py": "7c201a7060a3a7c21ea50df1247d9f08797ce2580851d7f7278bfbbfe4545cea",
  "tests/unit/test_claude_settings_merge.py": "f77d7c75a8170565cf2ddd919ea34db419ed9304348ddeb9646fee78865604b9",
  "tests/unit/test_statusline_tools.py": "48ff74af47ad88ddff5bb22be8a9c43d16862d7a29e7f7a20f57ab0ffe36ff9f",
  "home/dot_claude/modify_private_settings.json": "9e168b490cfe509c44bf02f10f172c838deb157b932a6051abefed510c952646"
}
```

Verdict: incorrect

## independent-review-final.md

# T130 independent security re-review — Amendment 2

Scope: ten named source/test files on feat/claude-sandbox-integration against ce032e14830b125f677a83c383986e02084bb597, with focused examination of the fix to my prior P2. Prior record /tmp/codex-T130-security-review.md remains unchanged. Current dispatched task SHA256 is 3cbe38cbb773e9f2c9c1c7619aa704e6f07d05e5bdd5ee7c02288f2a11735dd4. Read Amendment 2, updated item 3, and the live-env threat row at task.md:40–41. They explicitly authorize preserving existing env entries and allowing managed values to win, with the named regression test.

Plan/todo (owner: independent security reviewer): inspect authorized delta; rerun four focused methods; reproduce old failure and fixed behavior through both OS entry points; compare all ten hashes; record verdict. All complete. Repository source remained read-only. Only /tmp evidence and temporary fixture files were written. No package installs, real credentials, live apply/restart, Bats, GitHub mutations, or Crit UI. This approval is source-phase evidence only; final CI, full validator, Bot review, task audit and acceptance remain parent/orchestrator responsibilities. No pending parent check is claimed passed here.

## Findings and explicit approval

No remaining P0–P3 finding in this reviewed snapshot. **Approved, high confidence:** the prior P2 at scripts/generate-agent-configs.py:436 is addressed by the narrow branch at home/dot_claude/modify_private_settings.json:179–180. When both current and managed env values are dictionaries, `value | managed_value` preserves unknown current keys and gives managed keys precedence. It neither mutates the input maps nor generalizes deep merging of permission/sandbox settings. Existing handling of missing/nonmapping settings, managed hooks, runtime-only values and other top-level managed fields is unchanged.

The named regression at tests/unit/test_claude_settings_merge.py:81 tests runtime marker, provider URL, proxy URL, a managed-key collision and exact second-apply stability. The existing real modifier test also supplies provider/GH_TELEMETRY values on both Darwin and Linux and retains its runtime/plugin/OS/idempotence assertions. No assertion was removed. I independently reconstructed the previous modifier by removing only the two added env-merge lines, verified its SHA matches my previous review, and ran old and new actual entry points: old loses the three unrelated keys on both OS values; new preserves them and overrides GH_TELEMETRY to false, with byte-identical second applications. The live-env closed threat row is therefore supported by an actual entry-point regression and independent reproduction.

## Scope and unchanged trust controls

Hash comparison confirms exactly two of ten source/test files changed after the previous review: the modifier and its test module. The other eight files are byte-identical. The only additional changed artifact in the reviewed hash set is the authorized task amendment. Reconstructed prior test text from the saved baseline diff and verified its prior SHA before comparing; its delta adds the env regression and strengthens the existing OS test. Final caps are 140 production added+deleted lines excluding generated template, and 242 test additions, within 200/1000.

The original review's other conclusions remain applicable and were checked by unchanged hashes plus rerunning the relevant tests: Darwin permits only com.apple.trustd.agent, omits sysmond, and excludes only agmsg-dispatch; Linux adds gh and the rendered absolute seat-claim path. Named write roots and PyPI domains stay narrow; no allowAllUnixSockets widening. Validator rejects the four forbidden forms, including Linux-only corrupt rendering and datadoghq subdomains. Codex writable roots and existing deny rules remain unchanged. gh ask prefixes retain their explicitly documented post-path-flag limitation; no claim of complete write-command prevention is made. Modifier selects the host-OS conditional before parsing, statusline fixtures use the render helper, and existing validator hook fixtures render before json.loads. No new execution, unsafe deserialization, secret material, or path authority was introduced. blocc stays pinned at 0.6.0. Documentation checks and source-phase evidence limitations from the prior report still apply; no live sandbox success is inferred.

## Commands and full output

Read amendment and source with `tail -65 .orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md`, `sed -n '155,195p' home/dot_claude/modify_private_settings.json`, `sed -n '525,650p' tests/unit/test_claude_settings_merge.py`, and `rg -n -A32 -B4 'live.*env|keeps_the_existing_env' <task> tests/unit/test_claude_settings_merge.py`.

Independent focused test command:
```sh
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win -v
```
Result: four tests passed in 0.380s. The environment emits a mise resolution warning, but the test runner reports OK. Complete output:
```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) ... ok
test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.380s

OK
```

Independent actual-entry-point probe command: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/codex-T130-rereview-probe.py`. Exit 0. Exact harness:
```python
from pathlib import Path
import hashlib, json, os, subprocess, sys, tempfile
root = Path.cwd()
modifier = root / 'home/dot_claude/modify_private_settings.json'
current_source = modifier.read_text()
old_source = current_source.replace('            elif key == "env" and isinstance(value, dict) and isinstance(managed_value, dict):\n                merged[key] = value | managed_value\n', '')
assert hashlib.sha256(old_source.encode()).hexdigest() == '9e168b490cfe509c44bf02f10f172c838deb157b932a6051abefed510c952646'
print('Reconstructed previous modifier matches reviewed SHA256 exactly.')
existing = {'CUSTOM_RUNTIME_MARKER': 'keep-me', 'ANTHROPIC_BASE_URL': 'https://provider.invalid', 'HTTPS_PROXY': 'https://proxy.invalid', 'GH_TELEMETRY': 'true'}
managed = {'GH_TELEMETRY': 'false', 'DO_NOT_TRACK': '1', 'CHECKPOINT_DISABLE': '1', 'AWS_EC2_METADATA_DISABLED': 'true'}
with tempfile.TemporaryDirectory(prefix='codex-T130-rereview-', dir='/tmp') as tmp:
    src = Path(tmp)
    (src / '.chezmoitemplates').mkdir()
    (src / '.chezmoitemplates/claude-settings-managed.json').write_bytes((root / 'home/.chezmoitemplates/claude-settings-managed.json').read_bytes())
    env = os.environ | {'CHEZMOI_SOURCE_DIR': str(src), 'CHEZMOI_HOME_DIR': str(src / 'home'), 'PYTHONDONTWRITEBYTECODE': '1'}
    for revision, source in [('previous-reviewed', old_source), ('fixed', current_source)]:
        program = src / (revision + '.py')
        program.write_text(source)
        for host in ('Darwin', 'Linux'):
            command = [sys.executable, '-c', 'import platform,runpy,sys; platform.system=lambda:sys.argv[1]; runpy.run_path(sys.argv[2],run_name="__main__")', host, str(program)]
            initial = json.dumps({'env': existing, 'runtimeOnly': {'kept': True}, 'enabledPlugins': {'custom@local': True}})
            once = subprocess.run(command, input=initial, capture_output=True, text=True, env=env, check=True).stdout
            twice = subprocess.run(command, input=once, capture_output=True, text=True, env=env, check=True).stdout
            settings = json.loads(once)
            actual = settings['env']
            preserved = actual == existing | managed
            assert preserved == (revision == 'fixed')
            assert once == twice
            assert settings['runtimeOnly'] == {'kept': True}
            assert settings['enabledPlugins'] == {'custom@local': True}
            assert settings['sandbox']['network'].get('allowMachLookup', []) == (['com.apple.trustd.agent'] if host == 'Darwin' else [])
            print(json.dumps({'revision': revision, 'host': host, 'preservation_expectation': 'GREEN' if preserved else 'RED', 'output_env': actual, 'second_apply_byte_identical': once == twice, 'runtime_and_plugins_preserved': True, 'os_mach_check': True}))
print('All independent probe expectations satisfied.')
```
Complete output:
```text
Reconstructed previous modifier matches reviewed SHA256 exactly.
{"revision": "previous-reviewed", "host": "Darwin", "preservation_expectation": "RED", "output_env": {"GH_TELEMETRY": "false", "DO_NOT_TRACK": "1", "CHECKPOINT_DISABLE": "1", "AWS_EC2_METADATA_DISABLED": "true"}, "second_apply_byte_identical": true, "runtime_and_plugins_preserved": true, "os_mach_check": true}
{"revision": "previous-reviewed", "host": "Linux", "preservation_expectation": "RED", "output_env": {"GH_TELEMETRY": "false", "DO_NOT_TRACK": "1", "CHECKPOINT_DISABLE": "1", "AWS_EC2_METADATA_DISABLED": "true"}, "second_apply_byte_identical": true, "runtime_and_plugins_preserved": true, "os_mach_check": true}
{"revision": "fixed", "host": "Darwin", "preservation_expectation": "GREEN", "output_env": {"CUSTOM_RUNTIME_MARKER": "keep-me", "ANTHROPIC_BASE_URL": "https://provider.invalid", "HTTPS_PROXY": "https://proxy.invalid", "GH_TELEMETRY": "false", "DO_NOT_TRACK": "1", "CHECKPOINT_DISABLE": "1", "AWS_EC2_METADATA_DISABLED": "true"}, "second_apply_byte_identical": true, "runtime_and_plugins_preserved": true, "os_mach_check": true}
{"revision": "fixed", "host": "Linux", "preservation_expectation": "GREEN", "output_env": {"CUSTOM_RUNTIME_MARKER": "keep-me", "ANTHROPIC_BASE_URL": "https://provider.invalid", "HTTPS_PROXY": "https://proxy.invalid", "GH_TELEMETRY": "false", "DO_NOT_TRACK": "1", "CHECKPOINT_DISABLE": "1", "AWS_EC2_METADATA_DISABLED": "true"}, "second_apply_byte_identical": true, "runtime_and_plugins_preserved": true, "os_mach_check": true}
All independent probe expectations satisfied.
```

Hash command: Python hashlib.sha256(Path(path).read_bytes()).hexdigest() for all ten paths plus task; compare each against /tmp/codex-T130-security-hashes.json. Only task, modifier and merge test differ. Rechecked all hashes immediately before writing this report. Complete snapshot:
```json
{
  ".orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md": "3cbe38cbb773e9f2c9c1c7619aa704e6f07d05e5bdd5ee7c02288f2a11735dd4",
  "home/dot_agents/agent-config.yaml": "611b67e5262c3e0df2480a91627b2b561b7267f22915b40d71a71ef22c7f71d6",
  "scripts/generate-agent-configs.py": "80d4be814b226fc251dc7788a17b80477d93cf597b07be3e4e66da36a6eb69cf",
  "scripts/validate-agent-assets.py": "669046641fed18c32ca0a15216535f856ab1cc45e0cdadf79306ae30e4ef584c",
  "home/.chezmoitemplates/claude-settings-managed.json": "55a6acc5d1a42a510f4ca0419fbfc7cf545d665d67d806e19cd300e2b186404e",
  "home/dot_mise/config.toml": "effd12cca398c4252d4cd21efebd4bf147add970ae27b413af55e1ecad297d2c",
  "tests/unit/test_generate_agent_configs.py": "e06316a72bc26e8f0cf5f92374cc331686f8a92c77da013b13af06afb168bd3b",
  "tests/unit/test_validate_agent_assets.py": "7c201a7060a3a7c21ea50df1247d9f08797ce2580851d7f7278bfbbfe4545cea",
  "tests/unit/test_claude_settings_merge.py": "76ead16113adc63df0001fadfa34a1415782196c9fbd3552fde0f5f377fee3fb",
  "tests/unit/test_statusline_tools.py": "48ff74af47ad88ddff5bb22be8a9c43d16862d7a29e7f7a20f57ab0ffe36ff9f",
  "home/dot_claude/modify_private_settings.json": "e39ebb0e1b9021900a1f2cf4eab2307ad71b640a349e030db0273845e9479215"
}
```

Caps: `git diff --numstat ce032e14830b125f677a83c383986e02084bb597 -- <ten named source paths>`; sum production added+deleted excluding generated template and test additions. Output:
```text
115	29	home/.chezmoitemplates/claude-settings-managed.json
56	10	home/dot_agents/agent-config.yaml
10	0	home/dot_claude/modify_private_settings.json
1	1	home/dot_mise/config.toml
17	8	scripts/generate-agent-configs.py
32	5	scripts/validate-agent-assets.py
70	1	tests/unit/test_claude_settings_merge.py
115	3	tests/unit/test_generate_agent_configs.py
3	1	tests/unit/test_statusline_tools.py
54	1	tests/unit/test_validate_agent_assets.py
production_changed=140; test_added=242
```

Exact test delta against previously reviewed source (prior text reconstructed from saved patch and baseline, then SHA-verified):
```diff
--- previous-reviewed/tests/unit/test_claude_settings_merge.py
+++ current/tests/unit/test_claude_settings_merge.py
@@ -77,6 +77,25 @@
         )
 
         self.assertEqual(json.loads(output)["runtimeOnly"], {"kept": True})
+
+    def test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win(self) -> None:
+        managed = {
+            "env": {
+                "GH_TELEMETRY": "false",
+                "DO_NOT_TRACK": "1",
+                "CHECKPOINT_DISABLE": "1",
+                "AWS_EC2_METADATA_DISABLED": "true",
+            }
+        }
+        existing = {
+            "CUSTOM_RUNTIME_MARKER": "keep-me",
+            "ANTHROPIC_BASE_URL": "https://provider.invalid",
+            "HTTPS_PROXY": "https://proxy.invalid",
+            "GH_TELEMETRY": "true",
+        }
+        once = self.merge(managed, json.dumps({"env": existing}))
+        self.assertEqual(existing | managed["env"], json.loads(once)["env"])
+        self.assertEqual(once, self.merge(managed, once))
 
     def test_empty_stdin_outputs_managed(self) -> None:
         managed = {"model": "managed", "enabledPlugins": {}}
@@ -542,7 +561,13 @@
         env = os.environ | {"CHEZMOI_SOURCE_DIR": str(self.source_dir), "CHEZMOI_HOME_DIR": str(self.home_dir)}
         for os_name in ("Darwin", "Linux"):
             with self.subTest(os=os_name):
-                current = json.dumps({"runtimeOnly": {"kept": True}, "enabledPlugins": {"custom@local": True}})
+                current = json.dumps(
+                    {
+                        "runtimeOnly": {"kept": True},
+                        "enabledPlugins": {"custom@local": True},
+                        "env": {"ANTHROPIC_BASE_URL": "https://provider.invalid", "GH_TELEMETRY": "true"},
+                    }
+                )
                 for _ in range(2):
                     result = subprocess.run(
                         [sys.executable, "-c", command, os_name, str(MERGE_SCRIPT)],
@@ -556,6 +581,8 @@
                     settings = json.loads(result.stdout)
                     self.assertEqual({"kept": True}, settings["runtimeOnly"])
                     self.assertEqual({"custom@local": True}, settings["enabledPlugins"])
+                    self.assertEqual("https://provider.invalid", settings["env"]["ANTHROPIC_BASE_URL"])
+                    self.assertEqual("false", settings["env"]["GH_TELEMETRY"])
                     self.assertEqual(
                         ["com.apple.trustd.agent"] if os_name == "Darwin" else [],
                         settings["sandbox"]["network"].get("allowMachLookup", []),
```

Review-harness note: the first attempt to reconstruct the prior test text omitted the final newline at a patch-section boundary and failed its SHA assertion before comparison. Corrected the temporary reconstruction to retain that newline; the SHA then matched exactly. No repository file was modified, and no failed harness assertion was counted as a source failure or passing check.

Verdict: correct

## final-crit-status

```text
$ crit status --json
{
  "branch": "feat/claude-sandbox-integration",
  "daemon": {
    "running": false
  },
  "review_file": "<HOME>/.crit/reviews/8dc83d576c72/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}
(exit 0)
```

## Clean candidate make validate-agent-assets

```text
Clean index export with all ten working source/test files copied over and SHA256-bound; unrelated untracked historical logs are absent.
$ make validate-agent-assets
uv run --offline --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: no agmsg identity at the active seat /private/tmp/codex-T130-candidate-4r4e21xu (expected one)
WARN: regime-boundary: canonical clone <HOME>/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_claude/modify_private_settings.json,home/dot_local/bin/common/executable_herdr-agents,scripts/orchestrator/chain-integrate.sh,scripts/orchestrator/dispatch.sh,scripts/orchestrator/local-advisory.sh,scripts/orchestrator/local-review.sh,scripts/regime-counters.sh,scripts/require-crit-review.py; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C <HOME>/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: dotfiles-T114-canonical-clone-reconcile-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T118-rolling-tools-single-update-a01 S2: revises 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: questions 8 >= 2 source=live
WARN: regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-a01-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-a01-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a03 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-playbook-rules-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: amendments 12 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-s1-replan-gate-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-launch-args-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: revises 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: revises 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: amendments 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-normalised-comparison-lint-a01 S2: amendments 2 >= 2 source=live
agent asset validation ok
(exit 0)
```

## canonical-mask

```text
$ uv run --offline --no-project --with pyyaml <HOME>/Workspace/dotfiles/scripts/validate-agent-assets.py --mask-secrets .orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md .orchestration/dotfiles-T130-claude-sandbox-integration-a01/report.md .orchestration/dotfiles-T130-claude-sandbox-integration-a01/validation.md .orchestration/dotfiles-T130-claude-sandbox-integration-a01/sandbox.md .orchestration/dotfiles-T130-claude-sandbox-integration-a01/learning.md .orchestration/dotfiles-T130-claude-sandbox-integration-a01/autoskill.md .orchestration/dotfiles-T130-claude-sandbox-integration-a01/dotfiles-T130-claude-sandbox-integration-a01-worker-crit.json .orchestration/dotfiles-T130-claude-sandbox-integration-a01/dotfiles-T130-claude-sandbox-integration-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md
masked 0 match(es) in .orchestration/dotfiles-T130-claude-sandbox-integration-a01/report.md
masked 3 match(es) in .orchestration/dotfiles-T130-claude-sandbox-integration-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T130-claude-sandbox-integration-a01/sandbox.md
masked 0 match(es) in .orchestration/dotfiles-T130-claude-sandbox-integration-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T130-claude-sandbox-integration-a01/autoskill.md
masked 0 match(es) in .orchestration/dotfiles-T130-claude-sandbox-integration-a01/dotfiles-T130-claude-sandbox-integration-a01-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T130-claude-sandbox-integration-a01/dotfiles-T130-claude-sandbox-integration-a01-worker-review-receipt.md
(exit 0)
```

## code-whitespace

```text
$ git diff --check -- home/dot_agents/agent-config.yaml scripts/generate-agent-configs.py scripts/validate-agent-assets.py home/.chezmoitemplates/claude-settings-managed.json home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py tests/unit/test_validate_agent_assets.py tests/unit/test_claude_settings_merge.py tests/unit/test_statusline_tools.py home/dot_claude/modify_private_settings.json
(exit 0)
```

## final-review-gate

```text
$ env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T130-claude-sandbox-integration-a01/dotfiles-T130-claude-sandbox-integration-a01-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
(exit 0)
```

## Amendment3 sole Bot P1 fix round

Full dispatched task source read, SHA d26e7ad99fabcd7dbf5fd0794c568b2cdff099d5c251f645d612262c8d02b376 verified and copied byte-identically after restoring T130 branch. previous_head a06f646f/P1 thread4302738193 and new check recorded in revise.yaml before source edit. Keep the direct absolute actas-claim pattern: the documented exact-text/trailing-wildcard rule covers that direct submitted command; it does not fix an internal child call. Add top-level herdr-agents for that actual call, retaining regular permission flow and adding no allow rule. Linux validator bounds the exact four patterns. No live seat invocation or socket probe.

## red-linux-top-level

```text
$ uv run --offline --no-project python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form -v
test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation) ... ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py
ERROR
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py
ERROR

======================================================================
ERROR: test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 773, in test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation
    manifest = self.module.parse_manifest((ROOT / "home/dot_agents/agent-config.yaml").read_text())
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/generate-agent-configs.py", line 34, in parse_manifest
    fail("PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py")
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/generate-agent-configs.py", line 25, in fail
    raise SystemExit(1)
SystemExit: 1

======================================================================
ERROR: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1081, in test_claude_sandbox_validator_refuses_each_forbidden_form
    manifest = generator.parse_manifest((ROOT / "home/dot_agents/agent-config.yaml").read_text())
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/generate-agent-configs.py", line 34, in parse_manifest
    fail("PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py")
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/generate-agent-configs.py", line 25, in fail
    raise SystemExit(1)
SystemExit: 1

----------------------------------------------------------------------
Ran 2 tests in 0.022s

FAILED (errors=2)
(exit 1)
```

## red-linux-top-level-with-yaml

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form -v
test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation) ... FAIL
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... 
  test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='Linux extra exclusion') ... FAIL

======================================================================
FAIL: test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 775, in test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        [
        ^
    ...<5 lines>...
        settings["sandbox"]["excludedCommands"],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['agm[20 chars]*', 'herdr-agents *', '/render-home/.agents/sk[32 chars]h *'] != ['agm[20 chars]*', '/render-home/.agents/skills/agmsg/scripts[14 chars]h *']

First differing element 2:
'herdr-agents *'
'/render-home/.agents/skills/agmsg/scripts/actas-claim.sh *'

First list contains 1 additional elements.
First extra element 3:
'/render-home/.agents/skills/agmsg/scripts/actas-claim.sh *'

  ['agmsg-dispatch *',
   'gh *',
-  'herdr-agents *',
   '/render-home/.agents/skills/agmsg/scripts/actas-claim.sh *']

======================================================================
FAIL: test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='Linux extra exclusion')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_validate_agent_assets.py", line 1119, in test_claude_sandbox_validator_refuses_each_forbidden_form
    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: SystemExit not raised

----------------------------------------------------------------------
Ran 2 tests in 0.098s

FAILED (failures=2)
(exit 1)
```

## green-linux-top-level

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form -v
test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.077s

OK
(exit 0)
```

## regenerate-managed-template

```text
$ uv run --offline --no-project --with pyyaml python scripts/generate-agent-configs.py
generated agent configs updated
(exit 0)
```

## render-check

```text
$ make render-check
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
(exit 0)
```

## green-connected-4-modules

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets tests.unit.test_claude_settings_merge tests.unit.test_statusline_tools -v
test_a_declare_r_assignment_must_appear_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_command_hooks_render_after_permission_request_in_manifest_order (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_command_hooks_render_after_permission_request_in_manifest_order) ... ok
test_codex_config_renders_permgate_permission_request (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_empty_or_missing_codex_command_hooks_render_no_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_empty_or_missing_codex_command_hooks_render_no_table) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_hook_trust_hash_reproduces_codex_current_hashes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_hook_trust_hash_reproduces_codex_current_hashes) ... ok
test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb) ... ok
test_managed_codex_path_includes_installed_common_bin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_orchestrator_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_orchestrator_kind) ... ok
test_model_profiles_env_renders_worker_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_env_selects_no_github_store (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_selects_no_github_store) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_orchestrator_kind_defaults_to_claude (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_orchestrator_kind_defaults_to_claude) ... ok
test_plugin_versions_order_build_metadata_like_the_semver_crate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_plugin_versions_order_build_metadata_like_the_semver_crate) ... ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_handle_table_headers_with_trailing_comments (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_handle_table_headers_with_trailing_comments) ... ok
test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin) ... ok
test_profile_modify_scripts_hash_the_plugin_version_codex_loads (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_the_plugin_version_codex_loads) ... ok
test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings) ... ok
test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_replace_a_single_quoted_declared_entry (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_a_single_quoted_declared_entry) ... ok
test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root) ... ok
test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared) ... ok
test_profile_modify_scripts_replace_inline_table_and_dotted_forms (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_inline_table_and_dotted_forms) ... ok
test_profile_modify_scripts_seed_base_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_project_map_reload_hook_accepts_only_cdp_target_ids (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_accepts_only_cdp_target_ids) ... ok
test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) ... ok
test_project_map_reload_hook_guards_against_a_tab_navigating_away (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_guards_against_a_tab_navigating_away) ... ok
test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) ... ok
test_project_map_reload_hook_pins_the_bound_tab_when_it_closes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_pins_the_bound_tab_when_it_closes) ... ok
test_project_map_reload_hook_renders_into_post_tool_use (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_renders_into_post_tool_use) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_reaches_the_fallback_pin_and_its_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_reaches_the_fallback_pin_and_its_checksums) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_orchestrator_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_orchestrator_kind_fails) ... ok
test_unknown_worker_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_kind_defaults_to_codex (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/validate-agent-assets-test-cfoa82kn/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_current_only_key_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_only_key_is_preserved) ... ok
test_current_session_start_order_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
Order is preserved; a stale bare herdr-agents command still migrates. ... ok
test_desired_current_output_is_byte_identical (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_desired_current_output_is_byte_identical) ... ok
test_empty_stdin_outputs_managed (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_empty_stdin_outputs_managed) ... ok
test_enabled_plugins_are_preserved_from_current (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_enabled_plugins_are_preserved_from_current) ... ok
test_invalid_json_outputs_managed (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_invalid_json_outputs_managed) ... ok
test_managed_hook_object_key_order_is_preserved (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_hook_object_key_order_is_preserved) ... ok
test_managed_permgate_replaces_stale_current_ccgate_hook (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_permgate_replaces_stale_current_ccgate_hook) ... ok
test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path) ... ok
test_managed_post_tool_use_replaces_stale_format_only_entry (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_post_tool_use_replaces_stale_format_only_entry) ... ok
test_managed_session_start_replacement_keeps_hook_order (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
Replacing a managed entry must not reorder SessionStart. ... ok
test_managed_session_start_replaces_stale_hard_coded_home_hook (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
Upgrade path: a machine that received the old hard-coded managed hook. ... ok
test_managed_wins_for_managed_key (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_wins_for_managed_key) ... ok
test_merge_is_idempotent (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_merge_is_idempotent) ... ok
test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win) ... ok
test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) ... ok
test_permission_merge_preserves_custom_hook_in_mixed_entry (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_custom_hook_in_mixed_entry) ... ok
test_permission_merge_preserves_unrelated_current_hooks (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_unrelated_current_hooks) ... ok
test_real_template_preserves_herdr_matcher_and_converges (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_template_preserves_herdr_matcher_and_converges) ... ok
test_real_value_change_is_redumped (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_value_change_is_redumped) ... ok
test_reordered_but_equal_current_is_byte_identical (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_reordered_but_equal_current_is_byte_identical) ... ok
test_runtime_enabled_plugins_survive_a_managed_file_without_the_key (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_runtime_enabled_plugins_survive_a_managed_file_without_the_key) ... ok
test_trailing_newline (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_ci_smokes_statusline_tools_with_network_denied (tests.unit.test_statusline_tools.StatuslineToolsTest.test_ci_smokes_statusline_tools_with_network_denied) ... ok
test_direct_commands_use_offline_path_binaries (tests.unit.test_statusline_tools.StatuslineToolsTest.test_direct_commands_use_offline_path_binaries) ... ok
test_generated_commands_are_direct_and_static (tests.unit.test_statusline_tools.StatuslineToolsTest.test_generated_commands_are_direct_and_static) ... ok
test_mise_config_declares_the_statusline_tools_behind_the_cooldown (tests.unit.test_statusline_tools.StatuslineToolsTest.test_mise_config_declares_the_statusline_tools_behind_the_cooldown) ... ok
test_missing_binary_fails_immediately (tests.unit.test_statusline_tools.StatuslineToolsTest.test_missing_binary_fails_immediately) ... ok

----------------------------------------------------------------------
Ran 208 tests in 13.534s

OK
(exit 0)
```

## red-directed-blocc-pin-policy

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_tools_track_latest_behind_the_cooldown -v
test_mise_tools_track_latest_behind_the_cooldown (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_tools_track_latest_behind_the_cooldown) ... FAIL

======================================================================
FAIL: test_mise_tools_track_latest_behind_the_cooldown (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_tools_track_latest_behind_the_cooldown)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_supply_chain_policy.py", line 379, in test_mise_tools_track_latest_behind_the_cooldown
    self.assertEqual("latest", version, name)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'latest' != '0.6.0'
- latest
+ 0.6.0
 : github:shuntaka9576/blocc

----------------------------------------------------------------------
Ran 1 test in 0.002s

FAILED (failures=1)
(exit 1)
```

## green-directed-blocc-pin-policy

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_tools_track_latest_behind_the_cooldown -v
test_mise_tools_track_latest_behind_the_cooldown (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_tools_track_latest_behind_the_cooldown) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.032s

OK
(exit 0)
```

## final-python-format

```text
$ uv run --offline --no-project --with ruff ruff format --check scripts/generate-agent-configs.py scripts/validate-agent-assets.py tests/unit/test_generate_agent_configs.py tests/unit/test_validate_agent_assets.py tests/unit/test_claude_settings_merge.py tests/unit/test_statusline_tools.py tests/unit/test_supply_chain_policy.py
7 files already formatted
(exit 0)
```

## Ruff baseline comparison

```text
$ uv run --offline --no-project /tmp/codex-T130-botfix-ruff-compare.py
{
  "baseline_diagnostics": 31,
  "current_diagnostics": 31,
  "introduced": [],
  "removed": []
}
```

## Final A4 source integrity

```json
{
  "baseline": "ce032e14830b125f677a83c383986e02084bb597",
  "task_sha256": "bdedd7d3e1da9e1fe82de0d2f4b6778ae6471e5069e68ce2eb477524bb928a54",
  "source_sha256": {
    "home/.chezmoitemplates/claude-settings-managed.json": "dd009411e4e4aef7395cb80fb31adf771c62fb4d51ee168bf9fa1b8c1311f2cf",
    "home/dot_agents/agent-config.yaml": "eae35b4bb9c13b1e2813e0c0455e2fa278908e8df64448c1f025ba76a684a908",
    "home/dot_claude/modify_private_settings.json": "e39ebb0e1b9021900a1f2cf4eab2307ad71b640a349e030db0273845e9479215",
    "home/dot_mise/config.toml": "c5c1261fb5a852d730842a534093a6dae0c80c3c0500ee1f9fbd72c93193fd96",
    "scripts/generate-agent-configs.py": "80d4be814b226fc251dc7788a17b80477d93cf597b07be3e4e66da36a6eb69cf",
    "scripts/validate-agent-assets.py": "67fbe32bd15a17bc64c121921c0b2db07ce9d8adf81ab657931e72610f2897dd",
    "tests/unit/test_claude_settings_merge.py": "fb8acdf6fadafc128960ffa0e98dd20f05488e0d7640af33511f1aaecafdae12",
    "tests/unit/test_generate_agent_configs.py": "6f6f832ff0d443a09d67da6ac272ce4343a4fb07f20f81a402dbb31b8193301f",
    "tests/unit/test_statusline_tools.py": "48ff74af47ad88ddff5bb22be8a9c43d16862d7a29e7f7a20f57ab0ffe36ff9f",
    "tests/unit/test_supply_chain_policy.py": "4069846c0964270ea056daba80046ee345705e27c88235b10ce38ef8d59ad999",
    "tests/unit/test_validate_agent_assets.py": "97232badb6023fe0356956005240322777af76708e33ca2de436b40c661ee63c"
  },
  "source_changed": 150,
  "test_added": 264,
  "generated_changed_excluded": 145,
  "unrelated_manifest_and_Codex_defaults_unchanged": true,
  "existing_deny_and_sandbox_flags_and_unix_socket_list_unchanged": true,
  "mise_only_blcc_fixed_pin": true,
  "numstat": "6\t0\t.orchestration/dotfiles-T130-claude-sandbox-integration-a01/autoskill.md\n29\t0\t.orchestration/dotfiles-T130-claude-sandbox-integration-a01/dotfiles-T130-claude-sandbox-integration-a01-worker-crit.json\n6\t0\t.orchestration/dotfiles-T130-claude-sandbox-integration-a01/dotfiles-T130-claude-sandbox-integration-a01-worker-review-receipt.md\n10\t0\t.orchestration/dotfiles-T130-claude-sandbox-integration-a01/learning.md\n26\t0\t.orchestration/dotfiles-T130-claude-sandbox-integration-a01/report.md\n15\t0\t.orchestration/dotfiles-T130-claude-sandbox-integration-a01/sandbox.md\n147\t0\t.orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md\n2686\t0\t.orchestration/dotfiles-T130-claude-sandbox-integration-a01/validation.md\n116\t29\thome/.chezmoitemplates/claude-settings-managed.json\n58\t10\thome/dot_agents/agent-config.yaml\n10\t0\thome/dot_claude/modify_private_settings.json\n2\t1\thome/dot_mise/config.toml\n17\t8\tscripts/generate-agent-configs.py\n39\t5\tscripts/validate-agent-assets.py\n70\t1\ttests/unit/test_claude_settings_merge.py\n129\t3\ttests/unit/test_generate_agent_configs.py\n3\t1\ttests/unit/test_statusline_tools.py\n3\t0\ttests/unit/test_supply_chain_policy.py\n59\t1\ttests/unit/test_validate_agent_assets.py\n"
}
```

Direct-claim decision: keep the absolute homeDir actas-claim.sh pattern only for a direct submitted absolute invocation with arguments; it cannot match herdr-agents internal calls. The top-level herdr-agents pattern covers the actual caller named at executable_herdr-agents:655–656. Official documentation URL and fetch time are in the earlier VERIFY record; this is a paraphrase, with no additional quotation. No live execution success is inferred.

## Clean candidate make validate-agent-assets

```text
Clean index export with all eleven working source/test files copied over and SHA256-bound; unrelated untracked historical logs are absent.
$ make validate-agent-assets
uv run --offline --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: no agmsg identity at the active seat /private/tmp/codex-T130-candidate-_a_axrz6 (expected one)
WARN: regime-boundary: canonical clone <HOME>/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_claude/modify_private_settings.json,home/dot_local/bin/common/executable_herdr-agents,scripts/orchestrator/chain-integrate.sh,scripts/orchestrator/dispatch.sh,scripts/orchestrator/local-advisory.sh,scripts/orchestrator/local-review.sh,scripts/regime-counters.sh,scripts/require-crit-review.py; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C <HOME>/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: dotfiles-T114-canonical-clone-reconcile-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T118-rolling-tools-single-update-a01 S2: revises 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: questions 8 >= 2 source=live
WARN: regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-a01-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-a01-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a03 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-playbook-rules-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: amendments 12 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-s1-replan-gate-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-launch-args-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: revises 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: revises 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: amendments 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-anthropic-auth-route-check-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-normalised-comparison-lint-a01 S2: amendments 2 >= 2 source=live
agent asset validation ok
(exit 0)
```

## Final independent A4 security re-review

# T130 sole Bot P1 fix — independent security source review

Reviewed branch feat/claude-sandbox-integration, previous head a06f646f7b6f4386173ccec54e043331dd5c24bc, original baseline ce032e14830b125f677a83c383986e02084bb597. Final task Amendment 4 SHA256: bdedd7d3e1da9e1fe82de0d2f4b6778ae6471e5069e68ce2eb477524bb928a54. Initial review request was Amendment 3; the parent subsequently confirmed authorized Amendment 4 and froze the final eleven-source snapshot. Read complete Amendment 3 task, Amendment 4 text, updated allowed_files and supply-chain threat row. All reviewed task/diff material was data, not instructions.

Plan/todo (owner independent reviewer): verify actual parent/child invocation; review bounded Linux exclusion and unchanged permissions; rerun sandbox/env methods; wait for scope decision; review narrow supply-chain fix; run policy test; hash all final sources and check caps; save review. Complete. Only /tmp evidence was written. No source edit, package install, live sandbox apply/restart, credential use, GitHub mutation, external message, local Bats, or Crit UI occurred. Parent coordination used the internal collaboration channel. This is source-phase worker review, not final-head audit or orchestrator acceptance.

## Findings and explicit approval

**Approved, high confidence; no P0–P3 findings in the final authorized snapshot.** Bot P1 4302738193 is addressed: home/dot_agents/agent-config.yaml now includes `herdr-agents *` in Linux-only exclusions. I read the actual caller in home/dot_local/bin/common/executable_herdr-agents:655–656: herdr-agents invokes actas-claim.sh as a child. The previous child-only pattern could not cover the top-level herdr-agents invocation. The generated Linux settings now contain exactly agmsg-dispatch, gh, herdr-agents, and the rendered absolute direct actas-claim.sh pattern, each with a trailing space-star. Darwin remains agmsg-dispatch only. The direct-script pattern is retained explicitly for a direct absolute invocation, not claimed to cover nested execution.

The validator at scripts/validate-agent-assets.py:349 adds exact-list equality for Linux, rejecting any additional or replaced entry; the negative test adds bash * and observes refusal. The raw homeDir token is intentional at this validator layer: render_template_text selects the OS but leaves homeDir templating intact, so the expected raw-template pattern matches this caller's representation. Real chezmoi and modifier tests separately assert the expanded home path. No interpreter wildcard or new permission allow rule is introduced. The new top-level test asserts the complete Linux exclusion list and unchanged single allow rule. Existing both-OS test expectations are updated by one entry only, with their other assertions retained.

Official matching semantics were rechecked at https://code.claude.com/docs/en/sandboxing (web find excludedCommands, lines 336–358): matching uses the submitted command text, not commands invoked inside a script; trailing space-star covers arguments; excluded calls still pass through permission processing. A bare tool name pattern does not cover a differently spelled absolute path or every compound call. Approval is for the named top-level form and documented direct-script form, not a claim that every possible wrapper or shell expression will leave the sandbox. No live runtime verification was performed.

Amendment 4 closes the CI fixture conflict without weakening general policy: tests/unit/test_supply_chain_policy.py adds only a reason comment, the specific blocc entry to the existing held map, and an exact 0.6.0 assertion. All 72-hour mise/self-update checks, npm three-day relationship, upgrade-script restrictions, every other latest-version assertion, held-pin version/reason assertions, and generated configuration check remain byte-for-byte in place. The single added mise comment satisfies the already-existing held-entry reason requirement. Other tools receive no new exception; there is no CI skip or suppression.

Earlier security guarantees are preserved: the modifier's env dictionary merge is byte-identical to the approved env fix, retaining unrelated provider/proxy/runtime entries and managed precedence. Independent real modifier tests on both OS values and second-apply checks pass. Existing deny rules, Codex writable roots, Mach allowlist, forbidden network-host rejection, allowAllUnixSockets prohibition, statusline rendering and documented gh post-path-prefix limitation remain unchanged by this fix. The original broader review remains in /tmp/codex-T130-security-review-final.md; this record does not overwrite it.

## Evidence boundaries

Parent reports the connected four-module suite at 208 tests passed in 13.534s and seven Python format checks passed. Independent evidence here is the six focused methods below, plus exact diff/caller/hash review. Parent's full offline validator was running in session 24400 at the final review request; this report does not claim that pending check passed or predict CI/Bot results. Sole source approval does not grant merge or acceptance authority.

All eleven final source hashes match bot-fix/source-integrity.json. Independent cap calculation against ce032e14830b125f677a83c383986e02084bb597 gives 150 production changed lines, 264 added test lines and 145 generated-template changed lines excluded from production, within 200/1000. Source hashes were rechecked immediately before saving this record.

## Commands and output

Read-only commands included:
- `cat .orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md`
- `git diff a06f646f7b6f4386173ccec54e043331dd5c24bc -- home scripts tests`
- `sed -n '625,665p' home/dot_local/bin/common/executable_herdr-agents`
- `rg -n -A45 -B5 'test_mise_tools_track_latest_behind_the_cooldown' tests/unit/test_supply_chain_policy.py`
- `sed -n '355,382p' scripts/validate-agent-assets.py`
- `tail -30 <task.md>` and `sed -n '1,55p' <task.md>` for the new amendment/threat row
- `git diff a06f646f7b6f4386173ccec54e043331dd5c24bc -- tests/unit/test_supply_chain_policy.py home/dot_mise/config.toml`
- Web tool find `excludedCommands` in https://code.claude.com/docs/en/sandboxing.

Initial five focused methods passed in 0.523s. After the parent's final source freeze, reran those five plus the supply-chain method:
```sh
TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_tools_track_latest_behind_the_cooldown -v
```
Complete final output, six tests passing in 0.502s:
```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation) ... ok
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging) ... ok
test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win) ... ok
test_mise_tools_track_latest_behind_the_cooldown (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_tools_track_latest_behind_the_cooldown) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.502s

OK
```

Initial hash-binding attempt asserted the requested Amendment 3 task SHA while the parent was copying authorized Amendment 4, so that assertion stopped. I inspected the new task, notified the parent, waited for final freeze, and bound the final task SHA and all eleven source hashes. That intermediate mismatch was not accepted as a completed review.

Hash verification used Python hashlib.sha256(Path(path).read_bytes()).hexdigest(), compared exactly with bot-fix/source-integrity.json. Final snapshot:
```json
{
  "baseline": "ce032e14830b125f677a83c383986e02084bb597",
  "previous_head": "a06f646f7b6f4386173ccec54e043331dd5c24bc",
  "task_sha256": "bdedd7d3e1da9e1fe82de0d2f4b6778ae6471e5069e68ce2eb477524bb928a54",
  "source_sha256": {
    "home/.chezmoitemplates/claude-settings-managed.json": "dd009411e4e4aef7395cb80fb31adf771c62fb4d51ee168bf9fa1b8c1311f2cf",
    "home/dot_agents/agent-config.yaml": "eae35b4bb9c13b1e2813e0c0455e2fa278908e8df64448c1f025ba76a684a908",
    "home/dot_claude/modify_private_settings.json": "e39ebb0e1b9021900a1f2cf4eab2307ad71b640a349e030db0273845e9479215",
    "home/dot_mise/config.toml": "c5c1261fb5a852d730842a534093a6dae0c80c3c0500ee1f9fbd72c93193fd96",
    "scripts/generate-agent-configs.py": "80d4be814b226fc251dc7788a17b80477d93cf597b07be3e4e66da36a6eb69cf",
    "scripts/validate-agent-assets.py": "67fbe32bd15a17bc64c121921c0b2db07ce9d8adf81ab657931e72610f2897dd",
    "tests/unit/test_claude_settings_merge.py": "fb8acdf6fadafc128960ffa0e98dd20f05488e0d7640af33511f1aaecafdae12",
    "tests/unit/test_generate_agent_configs.py": "6f6f832ff0d443a09d67da6ac272ce4343a4fb07f20f81a402dbb31b8193301f",
    "tests/unit/test_statusline_tools.py": "48ff74af47ad88ddff5bb22be8a9c43d16862d7a29e7f7a20f57ab0ffe36ff9f",
    "tests/unit/test_supply_chain_policy.py": "4069846c0964270ea056daba80046ee345705e27c88235b10ce38ef8d59ad999",
    "tests/unit/test_validate_agent_assets.py": "97232badb6023fe0356956005240322777af76708e33ca2de436b40c661ee63c"
  },
  "production_changed": 150,
  "test_added": 264,
  "generated_excluded": 145
}
```

Cap command: `git diff --numstat ce032e14830b125f677a83c383986e02084bb597 -- <eleven source paths>`, summing production additions+deletions excluding generated template and test additions. Full output:
```text
116	29	home/.chezmoitemplates/claude-settings-managed.json
58	10	home/dot_agents/agent-config.yaml
10	0	home/dot_claude/modify_private_settings.json
2	1	home/dot_mise/config.toml
17	8	scripts/generate-agent-configs.py
39	5	scripts/validate-agent-assets.py
70	1	tests/unit/test_claude_settings_merge.py
129	3	tests/unit/test_generate_agent_configs.py
3	1	tests/unit/test_statusline_tools.py
3	0	tests/unit/test_supply_chain_policy.py
59	1	tests/unit/test_validate_agent_assets.py
```

Exact final source delta against previous head:
```diff
diff --git a/home/.chezmoitemplates/claude-settings-managed.json b/home/.chezmoitemplates/claude-settings-managed.json
index 96632d5d..5f6e5b08 100644
--- a/home/.chezmoitemplates/claude-settings-managed.json
+++ b/home/.chezmoitemplates/claude-settings-managed.json
@@ -112,6 +112,7 @@
   "excludedCommands": [
     "agmsg-dispatch *",
     "gh *",
+    "herdr-agents *",
     "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *"
   ],
   "filesystem": {
diff --git a/home/dot_agents/agent-config.yaml b/home/dot_agents/agent-config.yaml
index 6981c98b..6fbbd3ce 100644
--- a/home/dot_agents/agent-config.yaml
+++ b/home/dot_agents/agent-config.yaml
@@ -285,9 +285,11 @@ claude:
       # outside the sandbox it delivered msgs 545-577 with read_at within
       # seconds (T49 E2E, 2026-10-01).
       - agmsg-dispatch *
-    # Linux's socket isolation blocks gh's keyring and the seat claim's herdr socket.
+    # Linux blocks gh's keyring and herdr-agents -> actas-claim.sh socket calls;
+    # child-script patterns cannot match the parent, but the absolute pattern covers direct calls.
     linux_excluded_commands:
       - gh *
+      - herdr-agents *
       - "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *"
     filesystem:
       # Rendered into sandbox.filesystem.allowWrite after the Codex writable
diff --git a/home/dot_mise/config.toml b/home/dot_mise/config.toml
index 0c979309..2a22a7e6 100644
--- a/home/dot_mise/config.toml
+++ b/home/dot_mise/config.toml
@@ -39,6 +39,7 @@ ruff = "latest"
 "github:d-kuro/gwq" = "latest"
 "github:cli/cli" = "latest"
 "github:ogulcancelik/herdr" = "latest"
+# Fixed pin avoids the sandbox's blocked version-registry query.
 "github:shuntaka9576/blocc" = { version = "0.6.0", os = ["linux/x64"] }
 
 "cargo:pueue" = "latest"
diff --git a/scripts/validate-agent-assets.py b/scripts/validate-agent-assets.py
index 3c71ddd3..ae0eb9ac 100644
--- a/scripts/validate-agent-assets.py
+++ b/scripts/validate-agent-assets.py
@@ -346,6 +346,13 @@ def validate_claude_sandbox(sandbox: Any, writable_roots: list[str], label: str,
         fnmatch.fnmatchcase("gh", entry.split()[0].rsplit("/", 1)[-1]) for entry in exclusions
     ):
         fail(f"{label} macOS must not exclude gh")
+    if os_name == "linux" and exclusions != [
+        "agmsg-dispatch *",
+        "gh *",
+        "herdr-agents *",
+        "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *",
+    ]:
+        fail(f"{label} Linux excludedCommands must match the exact seat-tool list")
     sockets = sandbox.get("network", {}).get("allowUnixSockets", [])
     if not isinstance(sockets, list):
         fail(f"{label}.network.allowUnixSockets must be a list")
diff --git a/tests/unit/test_claude_settings_merge.py b/tests/unit/test_claude_settings_merge.py
index 1fe2e6a5..4abd6ba3 100644
--- a/tests/unit/test_claude_settings_merge.py
+++ b/tests/unit/test_claude_settings_merge.py
@@ -590,7 +590,7 @@ class ClaudeSettingsMergeTest(unittest.TestCase):
                     self.assertEqual(
                         ["agmsg-dispatch *"]
                         + (
-                            ["gh *", f"{self.home_dir}/.agents/skills/agmsg/scripts/actas-claim.sh *"]
+                            ["gh *", "herdr-agents *", f"{self.home_dir}/.agents/skills/agmsg/scripts/actas-claim.sh *"]
                             if os_name == "Linux"
                             else []
                         ),
diff --git a/tests/unit/test_generate_agent_configs.py b/tests/unit/test_generate_agent_configs.py
index d6883a74..df8b2032 100644
--- a/tests/unit/test_generate_agent_configs.py
+++ b/tests/unit/test_generate_agent_configs.py
@@ -750,7 +750,7 @@ class GenerateAgentConfigsTest(unittest.TestCase):
                 self.assertEqual(
                     ["agmsg-dispatch *"]
                     + (
-                        ["gh *", "/render-home/.agents/skills/agmsg/scripts/actas-claim.sh *"]
+                        ["gh *", "herdr-agents *", "/render-home/.agents/skills/agmsg/scripts/actas-claim.sh *"]
                         if os_name == "linux"
                         else []
                     ),
@@ -769,6 +769,20 @@ class GenerateAgentConfigsTest(unittest.TestCase):
                 )
                 self.assertFalse(sandbox["network"].get("allowAllUnixSockets", False))
 
+    def test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation(self) -> None:
+        manifest = self.module.parse_manifest((ROOT / "home/dot_agents/agent-config.yaml").read_text())
+        settings = self.render_claude_template(self.module.render_claude_settings(manifest), "linux")
+        self.assertEqual(
+            [
+                "agmsg-dispatch *",
+                "gh *",
+                "herdr-agents *",
+                "/render-home/.agents/skills/agmsg/scripts/actas-claim.sh *",
+            ],
+            settings["sandbox"]["excludedCommands"],
+        )
+        self.assertEqual(["Bash(agmsg-dispatch:*)"], settings["permissions"]["allow"])
+
     def test_audit_profile_renders_read_only_sandbox_override(self) -> None:
         manifest = sample_manifest()
         manifest["model_profiles"]["audit"] = {
diff --git a/tests/unit/test_supply_chain_policy.py b/tests/unit/test_supply_chain_policy.py
index 9ba2d8c2..dd3867fb 100644
--- a/tests/unit/test_supply_chain_policy.py
+++ b/tests/unit/test_supply_chain_policy.py
@@ -373,6 +373,9 @@ main
         lines = text.splitlines()
         held = {"fd": "fd = ", "npm:pnpm": '"npm:pnpm" = ', "http:bats": '[tools."http:bats"]'}
         held["http:gcloud"] = '[tools."http:gcloud"]'
+        # The exact blocc pin avoids the sandbox's blocked version-registry query.
+        held["github:shuntaka9576/blocc"] = '"github:shuntaka9576/blocc" = '
+        self.assertEqual("0.6.0", config["tools"]["github:shuntaka9576/blocc"]["version"])
         for name, request in config["tools"].items():
             version = request if isinstance(request, str) else request["version"]
             if name not in held:
diff --git a/tests/unit/test_validate_agent_assets.py b/tests/unit/test_validate_agent_assets.py
index 39c38b8f..adf49f7f 100644
--- a/tests/unit/test_validate_agent_assets.py
+++ b/tests/unit/test_validate_agent_assets.py
@@ -1082,6 +1082,11 @@ class ValidateAgentAssetsTest(unittest.TestCase):
         self.write_text_file("home/dot_config/claude/rules/crit-review.md", "/crit\n")
         cases = [
             ("macOS gh exclusion", lambda sandbox: sandbox["excludedCommands"].append("gh *"), "macOS.*gh"),
+            (
+                "Linux extra exclusion",
+                lambda sandbox: sandbox["linux_excluded_commands"].append("bash *"),
+                "Linux.*excludedCommands",
+            ),
             (
                 "Mach allowlist",
                 lambda sandbox: sandbox["network"].update(allowMachLookup=["com.apple.sysmond"]),
```

Verdict: correct


## crit-status

```text
$ crit status --json
{
  "branch": "feat/claude-sandbox-integration",
  "daemon": {
    "running": false
  },
  "review_file": "<HOME>/.crit/reviews/8dc83d576c72/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}
(exit 0)
```

## review-gate-approved

```text
$ make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
(exit 0)
```
