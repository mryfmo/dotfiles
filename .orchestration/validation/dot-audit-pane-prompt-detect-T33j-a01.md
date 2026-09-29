# T33j validation: dot-audit-pane-prompt-detect-T33j-a01 (revision 1)

## Mutation baseline: new tests against the unmodified origin/main script
```
herdr-agents == origin/main d7a5947
$ python3 -m unittest tests.unit.test_herdr_agents -k audit_trusts_a_shell -k audit_falls_back -k audit_waits_for_the_prompt -k audit_refuses_a_busy
FF.FFF
======================================================================
FAIL: test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info) (recent='~/project ❯ \n\n\n')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2846, in test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info
    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: audit pane w-old:p9 is busy (not at a shell prompt); refusing a second audit.


======================================================================
FAIL: test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info) (recent='codex output\n\n')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2847, in test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info
    self.assertIn("pane read w-old:p9 --source recent-unwrapped --lines 50", calls)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'pane read w-old:p9 --source recent-unwrapped --lines 50' not found in ['workspace list', 'pane list --workspace w-old', 'tab list --workspace w-old', 'pane list --workspace w-old', 'pane rename w-old:p9 audit', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9', 'pane process-info --pane w-old:p9']

======================================================================
FAIL: test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot) (state='shell')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2829, in test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: audit pane w-old:p9 is busy (not at a shell prompt); refusing a second audit.


======================================================================
FAIL: test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot) (state='shell-pid')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2829, in test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 0 : herdr-agents: audit pane w-old:p9 is busy (not at a shell prompt); refusing a second audit.


======================================================================
FAIL: test_audit_waits_for_the_prompt_on_a_new_audit_tab (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_waits_for_the_prompt_on_a_new_audit_tab)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_herdr_agents.py", line 2859, in test_audit_waits_for_the_prompt_on_a_new_audit_tab
    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 2 : Audit exit: 0
Audit evidence: /tmp/herdr-agents-test-akbeipgc/project/.orchestration/validation/audit-926d9f1.md
Audit last message: /tmp/herdr-agents-test-akbeipgc/project/.orchestration/validation/audit-926d9f1.md.last.md
Audit verdict source: transcript
Audit verdict: missing


----------------------------------------------------------------------
Ran 4 tests in 41.671s

FAILED (failures=5)
```

## make validate-agent-assets
```
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
```

## make unit-test (head and tail)
```
$ make unit-test
uv run python -m unittest discover -s tests/unit -v
test_bounded_scan_finishes_under_wall_limit (test_agent_session_staleness.AgentSessionStalenessTest.test_bounded_scan_finishes_under_wall_limit) ... ok
...

----------------------------------------------------------------------
Ran 525 tests in 88.626s

OK (skipped=1)
exit=0
```

## herdr-agents unit tests (tail)
```
$ python3 -m unittest tests.unit.test_herdr_agents
...
----------------------------------------------------------------------
Ran 126 tests in 64.203s

OK
```

## shellcheck / shfmt
```
$ shellcheck -x home/dot_local/bin/common/executable_herdr-agents
exit=0
$ shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents
exit=0
```

## git diff --stat / commit / branch
```
$ git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
 README.md                                         |  4 +-
 home/dot_local/bin/common/executable_herdr-agents | 46 ++++++++++----
 tests/unit/test_herdr_agents.py                   | 75 ++++++++++++++++++++++-
 3 files changed, 110 insertions(+), 15 deletions(-)
$ git -C .claude/worktrees/worker-c log --oneline -1 && git -C .claude/worktrees/worker-c rev-parse HEAD && git -C .claude/worktrees/worker-c ls-remote origin fix/audit-pane-prompt-detect
4b88402 fix(herdr-agents): decide "audit pane busy" from the foreground process
4b88402f2c8108d926f6720980dff387f16d9139
4b88402f2c8108d926f6720980dff387f16d9139	refs/heads/fix/audit-pane-prompt-detect
```

## PR
```
$ gh pr view 205 --json number,url,headRefName -q "\(.number) \(.url) \(.headRefName)"
205 https://github.com/mryfmo/dotfiles/pull/205 fix/audit-pane-prompt-detect
```

## CI
```
$ gh pr checks 205
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36500152586/job/109188823278	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/36500152583/job/109188823650	
private-bootstrap (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36500152583/job/109188823318	
private-bootstrap (ubuntu-latest, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36500152583/job/109188823610	
public-bootstrap (macos-14, client)	pass	8m2s	https://github.com/mryfmo/dotfiles/actions/runs/36500152583/job/109188823545	
public-bootstrap (ubuntu-latest, client)	pass	8m23s	https://github.com/mryfmo/dotfiles/actions/runs/36500152583/job/109188823743	
public-bootstrap (ubuntu-latest, server)	pass	6m53s	https://github.com/mryfmo/dotfiles/actions/runs/36500152583/job/109188823540	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36500152586/job/109188868548	
test (macos-14, client)	pass	3m27s	https://github.com/mryfmo/dotfiles/actions/runs/36500152586/job/109188867334	
test (ubuntu-latest, client)	pass	5m41s	https://github.com/mryfmo/dotfiles/actions/runs/36500152586/job/109188867421	
test (ubuntu-latest, server)	pass	2m51s	https://github.com/mryfmo/dotfiles/actions/runs/36500152586/job/109188867377	
validate	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/36500152649/job/109188823627	
exit=0
$ gh pr view 205 --json headRefOid -q .headRefOid
4b88402f2c8108d926f6720980dff387f16d9139
```

## CompactionDB
```
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T33j: herdr-agents decides \"audit pane busy\" from the pane's foreground process (shell = free), not from a visible-snapshot prompt regex, because background-tab visible snapshots can be stale (operator 2026-09-29)."
5a64a0ef-d6e0-404f-b95e-a12d291cbee1
```
