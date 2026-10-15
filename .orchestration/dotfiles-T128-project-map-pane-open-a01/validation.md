# Validation

Actual command output follows, with repository masking applied to local home paths before publication. Empty blocks mean no stdout/stderr.

## terminal-browser open --help (read-only, exit0)

```text
[1015/091324.272062:ERROR:electron/shell/common/mac/codesign_util.cc:79] task_name_for_pid: (os/kern) failure (5)
Usage: terminal-browser open [url] [options]

Opens the browser in the current pane. Pass --split to open it in a new
split pane instead.

The url can be a normal url, a localhost port, or a path to an html file.

Options:
  --split <direction>   Open in a new pane: right, left, down, up
  --size <fraction>     How much of the space the split takes (0.2 to 0.95)
  --ssh <user@host>     Perform all network requests through a remote server, then
                        proxy the result back to the local terminal-browser instance
  --allow-clipboard-read
                        Lets websites read from clipboard.
  --no-merge            Do not open the terminal-browser instance as a tab in a neighbor terminal-browser


Examples:
  terminal-browser open localhost:3000
  terminal-browser open ./report.html --split right
  terminal-browser open github.com/zenbu-labs --split down --size 0.4
  terminal-browser open --ssh dev@build-box localhost:8080
```

## scoped rg callers before edits

```text
home/.chezmoitemplates/claude-settings-managed.json:109:            "command": "~/.claude/hooks/project-map-reload.sh"
home/dot_agents/agent-config.yaml:280:    project_map_reload_hook: ~/.claude/hooks/project-map-reload.sh
scripts/generate-agent-configs.py:410:    if hooks.get("project_map_reload_hook"):
scripts/generate-agent-configs.py:414:                "command": hooks["project_map_reload_hook"],
scripts/check-agent-runtime.py:829:            SOURCE_ROOT / "dot_claude/hooks/executable_project-map-reload.sh",
scripts/check-agent-runtime.py:830:            HOME / ".claude/hooks/project-map-reload.sh",
tests/unit/test_generate_agent_configs.py:101:                "project_map_reload_hook": "~/.claude/hooks/project-map-reload.sh",
tests/unit/test_generate_agent_configs.py:1486:                        {"type": "command", "command": "~/.claude/hooks/project-map-reload.sh"},
tests/unit/test_generate_agent_configs.py:1494:        del manifest["claude"]["hooks"]["project_map_reload_hook"]
tests/unit/test_generate_agent_configs.py:1498:    def test_project_map_reload_hook_renders_into_post_tool_use(self) -> None:
tests/unit/test_generate_agent_configs.py:1508:                        {"type": "command", "command": "~/.claude/hooks/project-map-reload.sh"},
tests/unit/test_generate_agent_configs.py:1513:        del manifest["claude"]["hooks"]["project_map_reload_hook"]
tests/unit/test_generate_agent_configs.py:1527:    def test_project_map_reload_hook_acts_only_on_the_map_and_never_fails(self) -> None:
tests/unit/test_generate_agent_configs.py:1528:        hook = ROOT / "home/dot_claude/hooks/executable_project-map-reload.sh"
home/dot_claude/hooks/executable_project-map-reload.sh:3:# @file home/dot_claude/hooks/executable_project-map-reload.sh
```

## UV_CACHE_DIR=/private/tmp/codex-dot-a004-uv uv run python -m unittest tests.unit.test_generate_agent_configs -k project_map_reload -v (before implementation, expected exit1)

```text
test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) ... 
  test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='no browser', listing={'browsers': []}) ... FAIL
  test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='no map tab', listing={'browsers': [{'key': 'other-browser', 'cdpPort': 1111, 'tabs': [{'id': 1, 'url': 'https://example.com/', 'active': True, 'targetId': 'OTHER-TARGET'}]}]}) ... FAIL
  test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='null target', listing={'browsers': [{'cdpPort': 9222, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': None}]}]}) ... FAIL
  test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': None, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]}) ... FAIL
  test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': '9222', 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]}) ... FAIL
  test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': 0, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]}) ... FAIL
  test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': 65536, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]}) ... FAIL
  test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': 1.5, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]}) ... FAIL
  test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid target', listing={'browsers': [{'cdpPort': 9222, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': '--all'}]}]}) ... FAIL
test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) ... 
  test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) (case='no map') ... FAIL
  test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) (case='open failure') ... FAIL
  test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) (case='no browser') ... FAIL
test_project_map_reload_hook_renders_into_post_tool_use (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_renders_into_post_tool_use) ... ok

======================================================================
FAIL: test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='no browser', listing={'browsers': []})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1646, in test_project_map_reload_hook_acts_only_on_the_map_and_never_fails
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        expected_browser_calls,
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['ls --all --json'] != ['ls --all --json', 'open /var/folders/py/p9bt7jvj2g7_hh3cv[84 chars]rge']

Second list contains 1 additional elements.
First extra element 1:
'open /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html --split right --size 0.5 --no-merge'

- ['ls --all --json']
?                   ^

+ ['ls --all --json',
?                   ^

+  'open '
+  '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html '
+  '--split right --size 0.5 --no-merge']

======================================================================
FAIL: test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='no map tab', listing={'browsers': [{'key': 'other-browser', 'cdpPort': 1111, 'tabs': [{'id': 1, 'url': 'https://example.com/', 'active': True, 'targetId': 'OTHER-TARGET'}]}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1646, in test_project_map_reload_hook_acts_only_on_the_map_and_never_fails
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        expected_browser_calls,
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['ls --all --json'] != ['ls --all --json', 'open /var/folders/py/p9bt7jvj2g7_hh3cv[84 chars]rge']

Second list contains 1 additional elements.
First extra element 1:
'open /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html --split right --size 0.5 --no-merge'

- ['ls --all --json']
?                   ^

+ ['ls --all --json',
?                   ^

+  'open '
+  '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html '
+  '--split right --size 0.5 --no-merge']

======================================================================
FAIL: test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='null target', listing={'browsers': [{'cdpPort': 9222, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': None}]}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1646, in test_project_map_reload_hook_acts_only_on_the_map_and_never_fails
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        expected_browser_calls,
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['ls --all --json'] != ['ls --all --json', 'open /var/folders/py/p9bt7jvj2g7_hh3cv[84 chars]rge']

Second list contains 1 additional elements.
First extra element 1:
'open /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html --split right --size 0.5 --no-merge'

- ['ls --all --json']
?                   ^

+ ['ls --all --json',
?                   ^

+  'open '
+  '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html '
+  '--split right --size 0.5 --no-merge']

======================================================================
FAIL: test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': None, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1646, in test_project_map_reload_hook_acts_only_on_the_map_and_never_fails
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        expected_browser_calls,
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['ls --all --json'] != ['ls --all --json', 'open /var/folders/py/p9bt7jvj2g7_hh3cv[84 chars]rge']

Second list contains 1 additional elements.
First extra element 1:
'open /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html --split right --size 0.5 --no-merge'

- ['ls --all --json']
?                   ^

+ ['ls --all --json',
?                   ^

+  'open '
+  '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html '
+  '--split right --size 0.5 --no-merge']

======================================================================
FAIL: test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': '9222', 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1646, in test_project_map_reload_hook_acts_only_on_the_map_and_never_fails
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        expected_browser_calls,
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['ls --all --json'] != ['ls --all --json', 'open /var/folders/py/p9bt7jvj2g7_hh3cv[84 chars]rge']

Second list contains 1 additional elements.
First extra element 1:
'open /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html --split right --size 0.5 --no-merge'

- ['ls --all --json']
?                   ^

+ ['ls --all --json',
?                   ^

+  'open '
+  '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html '
+  '--split right --size 0.5 --no-merge']

======================================================================
FAIL: test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': 0, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1646, in test_project_map_reload_hook_acts_only_on_the_map_and_never_fails
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        expected_browser_calls,
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['ls --all --json'] != ['ls --all --json', 'open /var/folders/py/p9bt7jvj2g7_hh3cv[84 chars]rge']

Second list contains 1 additional elements.
First extra element 1:
'open /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html --split right --size 0.5 --no-merge'

- ['ls --all --json']
?                   ^

+ ['ls --all --json',
?                   ^

+  'open '
+  '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html '
+  '--split right --size 0.5 --no-merge']

======================================================================
FAIL: test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': 65536, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1646, in test_project_map_reload_hook_acts_only_on_the_map_and_never_fails
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        expected_browser_calls,
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['ls --all --json'] != ['ls --all --json', 'open /var/folders/py/p9bt7jvj2g7_hh3cv[84 chars]rge']

Second list contains 1 additional elements.
First extra element 1:
'open /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html --split right --size 0.5 --no-merge'

- ['ls --all --json']
?                   ^

+ ['ls --all --json',
?                   ^

+  'open '
+  '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html '
+  '--split right --size 0.5 --no-merge']

======================================================================
FAIL: test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid port', listing={'browsers': [{'cdpPort': 1.5, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': 'MAP-CDP-TARGET'}]}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1646, in test_project_map_reload_hook_acts_only_on_the_map_and_never_fails
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        expected_browser_calls,
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['ls --all --json'] != ['ls --all --json', 'open /var/folders/py/p9bt7jvj2g7_hh3cv[84 chars]rge']

Second list contains 1 additional elements.
First extra element 1:
'open /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html --split right --size 0.5 --no-merge'

- ['ls --all --json']
?                   ^

+ ['ls --all --json',
?                   ^

+  'open '
+  '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html '
+  '--split right --size 0.5 --no-merge']

======================================================================
FAIL: test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) (case='invalid target', listing={'browsers': [{'cdpPort': 9222, 'tabs': [{'id': 7, 'url': 'file:///var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html', 'active': False, 'targetId': '--all'}]}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1646, in test_project_map_reload_hook_acts_only_on_the_map_and_never_fails
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        expected_browser_calls,
        ^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['ls --all --json'] != ['ls --all --json', 'open /var/folders/py/p9bt7jvj2g7_hh3cv[84 chars]rge']

Second list contains 1 additional elements.
First extra element 1:
'open /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html --split right --size 0.5 --no-merge'

- ['ls --all --json']
?                   ^

+ ['ls --all --json',
?                   ^

+  'open '
+  '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmpe20iuozb/.project-map/index.html '
+  '--split right --size 0.5 --no-merge']

======================================================================
FAIL: test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) (case='no map')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1740, in test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        [json.loads(line) for line in browser_calls.read_text().splitlines()], expected_browser
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: [['ls[16 chars]son']] != [['ls[16 chars]son'], ['open', '/var/folders/py/p9bt7jvj2g7_h[120 chars]ge']]

Second list contains 1 additional elements.
First extra element 1:
['open', '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmptfzkyhd1/map with spaces/.project-map/index.html', '--split', 'right', '--size', '0.5', '--no-merge']

- [['ls', '--all', '--json']]
?                           ^

+ [['ls', '--all', '--json'],
?                           ^

+  ['open',
+   '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmptfzkyhd1/map with '
+   'spaces/.project-map/index.html',
+   '--split',
+   'right',
+   '--size',
+   '0.5',
+   '--no-merge']]

======================================================================
FAIL: test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) (case='open failure')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1740, in test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        [json.loads(line) for line in browser_calls.read_text().splitlines()], expected_browser
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: [['ls[16 chars]son']] != [['ls[16 chars]son'], ['open', '/var/folders/py/p9bt7jvj2g7_h[120 chars]ge']]

Second list contains 1 additional elements.
First extra element 1:
['open', '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmptfzkyhd1/map with spaces/.project-map/index.html', '--split', 'right', '--size', '0.5', '--no-merge']

- [['ls', '--all', '--json']]
?                           ^

+ [['ls', '--all', '--json'],
?                           ^

+  ['open',
+   '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmptfzkyhd1/map with '
+   'spaces/.project-map/index.html',
+   '--split',
+   'right',
+   '--size',
+   '0.5',
+   '--no-merge']]

======================================================================
FAIL: test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) (case='no browser')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_generate_agent_configs.py", line 1740, in test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        [json.loads(line) for line in browser_calls.read_text().splitlines()], expected_browser
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: [['ls[16 chars]son']] != [['ls[16 chars]son'], ['open', '/var/folders/py/p9bt7jvj2g7_h[120 chars]ge']]

Second list contains 1 additional elements.
First extra element 1:
['open', '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmptfzkyhd1/map with spaces/.project-map/index.html', '--split', 'right', '--size', '0.5', '--no-merge']

- [['ls', '--all', '--json']]
?                           ^

+ [['ls', '--all', '--json'],
?                           ^

+  ['open',
+   '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmptfzkyhd1/map with '
+   'spaces/.project-map/index.html',
+   '--split',
+   'right',
+   '--size',
+   '0.5',
+   '--no-merge']]

----------------------------------------------------------------------
Ran 3 tests in 2.039s

FAILED (failures=12)
```

## UV_CACHE_DIR=/private/tmp/codex-dot-a004-uv uv run python -m unittest tests.unit.test_generate_agent_configs -k project_map_reload -v (after implementation, exit0)

```text
test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) ... ok
test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) ... ok
test_project_map_reload_hook_renders_into_post_tool_use (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_renders_into_post_tool_use) ... ok

----------------------------------------------------------------------
Ran 3 tests in 1.856s

OK
```

## shellcheck home/dot_claude/hooks/executable_project-map-reload.sh (exit0)

```text
```

## UV_CACHE_DIR=/private/tmp/codex-dot-a004-uv make render-check (exit0)

```text
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
```

## crit status --json

```text
{
  "branch": "feat/project-map-pane-open",
  "daemon": {
    "running": false
  },
  "review_file": "~/.crit/reviews/d2c047ee5d5a/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}
```

## crit comments --all --json <reported review path> (exit1; data missing)

```text
stat ~/.crit/reviews/d2c047ee5d5a/review.json: no such file or directory
```

## make require-crit-review (before evidence; expected exit2)

```text
Native agent review required before completion.
- agent lifecycle path changed: home/dot_agents/skills/project-map/SKILL.md
- broad diff touches 7 files
- broad diff changes 247 lines
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
```

## git diff --numstat (working tree)

```text
1	1	home/dot_agents/skills/project-map/SKILL.md
8	2	home/dot_claude/hooks/executable_project-map-reload.sh
1	1	home/dot_config/claude/rules/project-map.md
104	1	tests/unit/test_generate_agent_configs.py
```

## git rev-parse HEAD origin/main (exit0)

```text
727180dbc33f50b8934c2f2ed229d1c6a744ce0d
727180dbc33f50b8934c2f2ed229d1c6a744ce0d
```

## git merge-base --is-ancestor e3006da7 HEAD (exit0)

```text
```

## shasum -a 256 .orchestration/dotfiles-T128-project-map-pane-open-a01/task.md (exit0)

```text
a2c1196e1f0ba873543683f49e89f2d27629d92c2edb3e076e099efc5d81842f  .orchestration/dotfiles-T128-project-map-pane-open-a01/task.md
```

## ruff format --check tests/unit/test_generate_agent_configs.py (exit0)

```text
1 file already formatted
```

## prettier --check home/dot_config/claude/rules/project-map.md home/dot_agents/skills/project-map/SKILL.md (exit0)

```text
Checking formatting...
All matched files use Prettier code style!
```

## git diff --check (exit0)

```text
```

## AGENT_REVIEWED=1 REVIEW_EVIDENCE=<worker receipt> make require-crit-review (exit0)

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```
