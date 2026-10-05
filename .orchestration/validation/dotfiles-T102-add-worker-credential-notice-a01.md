# T102 validation

pr: 285
pr_url: https://github.com/mryfmo/dotfiles/pull/285
head: 015929c8c66103e042c834aff28618ec3634b257
bot: orchestrator-side

UV_CACHE_DIR=/tmp/dotfiles-T102-uv-cache points cache writes inside sandbox. All outputs below are verbatim except repository masker normalization of home paths.

## Test-first red

```text
FFF.
======================================================================
FAIL: test_add_worker_notices_missing_github_credential (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_notices_missing_github_credential)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2761, in test_add_worker_notices_missing_github_credential
    self.assertEqual(result.stderr.splitlines().count(notice), 1, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 

======================================================================
FAIL: test_restart_worker_notices_missing_github_credential (tests.unit.test_herdr_agents.HerdrAgentsTest.test_restart_worker_notices_missing_github_credential)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2773, in test_restart_worker_notices_missing_github_credential
    self.assertEqual(result.stderr.splitlines().count(notice), 1, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 

======================================================================
FAIL: test_full_mode_notices_missing_github_credential (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_notices_missing_github_credential)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 2783, in test_full_mode_notices_missing_github_credential
    self.assertEqual(result.stderr.splitlines().count(notice), 1, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : Codex loads the new repo hook only after the project .codex layer is trusted; run /hooks or trust the repo in Codex.
First-time Claude Code agmsg setup may stop one same-repo watcher once; the hooks apply in the next Claude Code session.
Multiple agmsg Claude Code identities are registered for /tmp/herdr-agents-test-1ubt861q/project; worker identity is ambiguous.


----------------------------------------------------------------------
Ran 4 tests in 3.881s

FAILED (failures=3)
```

## Four targeted tests after implementation

```text
....
----------------------------------------------------------------------
Ran 4 tests in 3.910s

OK
```

`git diff origin/main --stat | tail -5`
```text
 README.md                                         |  2 +-
 home/dot_local/bin/common/executable_herdr-agents | 12 +++++
 tests/unit/test_herdr_agents.py                   | 63 +++++++++++++++++++++++
 3 files changed, 76 insertions(+), 1 deletion(-)
```
command_exit=0

`bash -n home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"`
```text
rc=0
```
command_exit=0

`shellcheck home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"`
```text
rc=0
```
command_exit=0

`mise x node npm:prettier -- prettier --check README.md 2>&1 | tail -2`
```text
Checking formatting...
All matched files use Prettier code style!
```
command_exit=0

`mise x ruff -- ruff format --config ruff.toml --check tests/unit/test_herdr_agents.py`
```text
1 file already formatted
```
command_exit=0

`git diff --check`
```text
```
command_exit=0

`uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"`
```text
Installed 1 package in 2ms
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T101-codex-worker-profile-default-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T82b-codex-hook-trust-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T101-codex-worker-profile-default-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T82b-codex-hook-trust-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T101-codex-worker-profile-default-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T82b-codex-hook-trust-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T101-codex-worker-profile-default-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T82b-codex-hook-trust-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T101-codex-worker-profile-default-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T82b-codex-hook-trust-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T101-codex-worker-profile-default-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T102-add-worker-credential-notice-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T82b-codex-hook-trust-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/codex-usage-2026-10-05.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-audit-462bbb1.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-audit-462bbb1.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-00a5b09.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-00a5b09.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-2552205.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-2552205.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-315e739.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-315e739.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-a6c997b.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-a6c997b.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-ad05e8b.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-ad05e8b.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-c54fdc0.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-c54fdc0.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-d870215.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-d870215.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-f6e99ba.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-audit-f6e99ba.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T82b-codex-hook-trust-pins-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/e2e-macos-installers.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T102-add-worker-credential-notice-a01.md
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-standard-dot-a006 (herdr-agents --remove-worker)
agent asset validation ok
rc=0
```

`uv run --no-project python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3`
```text
Ran 234 tests in 158.134s

OK
```
source_command_exit=0

`AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dotfiles-T102-add-worker-credential-notice-a01-worker-review-receipt.md make require-crit-review`
```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```
command_exit=0

`make unit-test 2>&1 | tail -3`
```text
Ran 881 tests in 226.703s

OK
```
source_command_exit=0

`git log -1 --format='%H %s'`
```text
015929c8c66103e042c834aff28618ec3634b257 feat(agents): notify when worker GitHub credentials are missing
```
command_exit=0

`git rev-parse HEAD`
```text
015929c8c66103e042c834aff28618ec3634b257
```
command_exit=0

`GIT_TERMINAL_PROMPT=0 git push origin feat/add-worker-credential-notice`
```text
remote: 
remote: Create a pull request for 'feat/add-worker-credential-notice' on GitHub by visiting:        
remote:      https://github.com/mryfmo/dotfiles/pull/new/feat/add-worker-credential-notice        
remote: 
To github.com:mryfmo/dotfiles.git
 * [new branch]        feat/add-worker-credential-notice -> feat/add-worker-credential-notice
```
command_exit=0

PR number, CI, Bot wait and PR feedback sweep: orchestrator-side per task; worker performs no gh API operations.

## PONG decision 1 handoff

Orchestrator message 1777 records PR #285 opened on head 015929c8 and assigns checks/Bot wait/sweep to orchestrator. Worker updated report and validation without further push. No worker claim of CI/Bot completion.
