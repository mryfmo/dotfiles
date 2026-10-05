# Validation: dotfiles-T98b-runner-home-and-review-body-a01

- **task_rev:** `sha256:0021ef8c5554fc15aaecf9d6fa418675f7a43c3c57c13637bb32f9bd7e56f5c2`; it matches the dispatched task_rev.
- **PR:** #280.
- **Final head:** `70f060e74c64e3da3f7dfa251f98d9e43a8b5105` (diff head and final head; main is still `58f7594f`).
- **Output:** every block below is verbatim and in full, with its real exit code; the paths were masked to `~` after writing.

## Task validation commands

In the `HOME=~` line, `$HOME` in `UV_CACHE_DIR` was substituted with the real home, as the task says.

```
$ git diff origin/main --stat | tail -5
 home/dot_agents/skills/agmsg-orchestration/SKILL.md |  4 +++-
 scripts/validate-agent-assets.py                    |  3 +++
 tests/unit/test_agmsg_orchestration_docs.py         |  2 ++
 tests/unit/test_validate_agent_assets.py            | 13 +++++++++++++
 4 files changed, 21 insertions(+), 1 deletion(-)
exit=0
```

```
$ uv run --no-project python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
Ran 110 tests in 1.463s

OK
exit=0
```

```
$ make unit-test 2>&1 | tail -3
Ran 876 tests in 219.097s

OK (skipped=1)
exit=0
```

```
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T98b-runner-home-and-review-body-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/e2e-claude-claude-linux.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/e2e-claude-codex-linux.md
agent asset validation ok
rc=0
exit=0
```

```
$ HOME=~ UV_CACHE_DIR=~/.cache/uv uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T98b-runner-home-and-review-body-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/e2e-claude-claude-linux.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/e2e-claude-codex-linux.md
agent asset validation ok
rc=0
exit=0
```

```
$ wc -w home/dot_config/claude/rules/agmsg-orchestration.md
429 home/dot_config/claude/rules/agmsg-orchestration.md
exit=0
```

Extra checks:

```
$ make render-check
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0
```

```
$ git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check
43 files already formatted
exit=0
```

### Tasks 7–8 (CI, mergeable state)

```
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
Refreshing checks status every 30 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pass	15m36s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pass	15m36s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
watch exit=0
```

```
$ gh pr checks 280
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693604508	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604781	
private-bootstrap (ubuntu-24.04, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604605	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604783	
public-bootstrap (macos-14, client)	pass	10m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604645	
public-bootstrap (ubuntu-24.04, client)	pass	7m15s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604319	
public-bootstrap (ubuntu-24.04, server)	pass	5m35s	https://github.com/mryfmo/dotfiles/actions/runs/37288664412/job/111693604660	
test (macos-14, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692799	
test (ubuntu-24.04, client)	pass	15m36s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692730	
test (ubuntu-24.04, server)	pass	4m41s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692825	
test (ubuntu-26.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/37288664387/job/111693692895	
validate	pass	1m16s	https://github.com/mryfmo/dotfiles/actions/runs/37288664423/job/111693604911	
exit=0
```

```
$ gh api repos/mryfmo/dotfiles/pulls/280 --jq '.mergeable_state'
clean
exit=0
```

## Re-mask of all tracked `.orchestration` files (item 1), full output

```
$ git ls-files -z .orchestration | xargs -0 uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets
masked 0 match(es) in .orchestration/acceptance/T10-herdr-files-pane.md
masked 0 match(es) in .orchestration/acceptance/T11-agmsg-join-unique-identity-guard.md
masked 0 match(es) in .orchestration/acceptance/T13-agmsg-orchestration-rule-file.md
masked 0 match(es) in .orchestration/acceptance/T14-t13-pr-lifecycle.md
masked 0 match(es) in .orchestration/acceptance/T15-herdr-lazy-start-attach-layout.md
masked 0 match(es) in .orchestration/acceptance/T16-herdr-attach-layout-order-repair.md
masked 0 match(es) in .orchestration/acceptance/T17-herdr-attach-agmsg-bootstrap.md
masked 0 match(es) in .orchestration/acceptance/T18-herdr-agents-two-pane.md
masked 0 match(es) in .orchestration/acceptance/T19-herdr-file-viewer-popup-config.md
masked 0 match(es) in .orchestration/acceptance/T21-model-profiles-pr.md
masked 0 match(es) in .orchestration/acceptance/T22-doctor-settings-idempotency.md
masked 0 match(es) in .orchestration/acceptance/T23-agmsg-nudge-guidance.md
masked 0 match(es) in .orchestration/acceptance/T24-usage-review-automation.md
masked 0 match(es) in .orchestration/acceptance/T25-permgate-harness.md
masked 0 match(es) in .orchestration/acceptance/T26-pr86-herdr-rebase.md
masked 0 match(es) in .orchestration/acceptance/T27-pr87-npm-allow-scripts-rebase.md
masked 0 match(es) in .orchestration/acceptance/T28-ccgate-removal-permgate-deploy.md
masked 0 match(es) in .orchestration/acceptance/T36-understand-anything-analysis.md
masked 0 match(es) in .orchestration/acceptance/T37-understand-anything-codex-dist.md
masked 0 match(es) in .orchestration/acceptance/T38-evidence-sync.md
masked 0 match(es) in .orchestration/acceptance/T40-understand-anything-search-first.md
masked 0 match(es) in .orchestration/acceptance/T41-remove-cognee.md
masked 0 match(es) in .orchestration/acceptance/T42-zero-tail-evidence-sync.md
masked 0 match(es) in .orchestration/acceptance/T43-compactiondb-integration.md
masked 0 match(es) in .orchestration/acceptance/T44-marker-extraction-redesign.md
masked 0 match(es) in .orchestration/acceptance/T45.md
masked 0 match(es) in .orchestration/acceptance/T46.md
masked 0 match(es) in .orchestration/acceptance/T47.md
masked 0 match(es) in .orchestration/acceptance/T48.md
masked 0 match(es) in .orchestration/acceptance/T48b.md
masked 0 match(es) in .orchestration/acceptance/T48c.md
masked 0 match(es) in .orchestration/acceptance/T49.md
masked 0 match(es) in .orchestration/acceptance/T50.md
masked 0 match(es) in .orchestration/acceptance/T51a.md
masked 0 match(es) in .orchestration/acceptance/T52.md
masked 0 match(es) in .orchestration/acceptance/T53.md
masked 0 match(es) in .orchestration/acceptance/T54.md
masked 0 match(es) in .orchestration/acceptance/T55.md
masked 0 match(es) in .orchestration/acceptance/T56.md
masked 0 match(es) in .orchestration/acceptance/T56b.md
masked 0 match(es) in .orchestration/acceptance/T57.md
masked 0 match(es) in .orchestration/acceptance/T58.md
masked 0 match(es) in .orchestration/acceptance/T59.md
masked 0 match(es) in .orchestration/acceptance/T59b.md
masked 0 match(es) in .orchestration/acceptance/T60.md
masked 0 match(es) in .orchestration/acceptance/T61a.md
masked 0 match(es) in .orchestration/acceptance/T61b.md
masked 0 match(es) in .orchestration/acceptance/T62.md
masked 0 match(es) in .orchestration/acceptance/T62b.md
masked 0 match(es) in .orchestration/acceptance/T62c.md
masked 0 match(es) in .orchestration/acceptance/T63.md
masked 0 match(es) in .orchestration/acceptance/T64.md
masked 0 match(es) in .orchestration/acceptance/T64b.md
masked 0 match(es) in .orchestration/acceptance/T65.md
masked 0 match(es) in .orchestration/acceptance/T65b.md
masked 0 match(es) in .orchestration/acceptance/T66.md
masked 0 match(es) in .orchestration/acceptance/T66b.md
masked 0 match(es) in .orchestration/acceptance/T66c.md
masked 0 match(es) in .orchestration/acceptance/T66d.md
masked 0 match(es) in .orchestration/acceptance/T66e.md
masked 0 match(es) in .orchestration/acceptance/T67.md
masked 0 match(es) in .orchestration/acceptance/T67b.md
masked 0 match(es) in .orchestration/acceptance/T67c.md
masked 0 match(es) in .orchestration/acceptance/T67d.md
masked 0 match(es) in .orchestration/acceptance/T67e.md
masked 0 match(es) in .orchestration/acceptance/T68.md
masked 0 match(es) in .orchestration/acceptance/T68b.md
masked 0 match(es) in .orchestration/acceptance/T68c.md
masked 0 match(es) in .orchestration/acceptance/T69.md
masked 0 match(es) in .orchestration/acceptance/T70.md
masked 0 match(es) in .orchestration/acceptance/T74.md
masked 0 match(es) in .orchestration/acceptance/T76.md
masked 0 match(es) in .orchestration/acceptance/T76b.md
masked 0 match(es) in .orchestration/acceptance/T79-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T79b-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T80-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T81-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T83-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T83b-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T84-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T84b-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T84c-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T85-acceptance.md
masked 0 match(es) in .orchestration/acceptance/T86-herdr-agents-082-api-port.md
masked 0 match(es) in .orchestration/acceptance/T87-boundary-bookkeeping-147.md
masked 0 match(es) in .orchestration/acceptance/WP-A.md
masked 0 match(es) in .orchestration/acceptance/WP-B.md
masked 0 match(es) in .orchestration/acceptance/WP-C.md
masked 0 match(es) in .orchestration/acceptance/WP-D.md
masked 0 match(es) in .orchestration/acceptance/WP-E.md
masked 0 match(es) in .orchestration/acceptance/WP-F.md
masked 0 match(es) in .orchestration/acceptance/WP-G.md
masked 0 match(es) in .orchestration/acceptance/WP-H.md
masked 0 match(es) in .orchestration/acceptance/WP-I.md
masked 0 match(es) in .orchestration/acceptance/WP-J.md
masked 0 match(es) in .orchestration/acceptance/WP-K.md
masked 0 match(es) in .orchestration/acceptance/WP-L.md
masked 0 match(es) in .orchestration/acceptance/WP-M.md
masked 0 match(es) in .orchestration/acceptance/dot-adh-baseline-T6-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-agmsg-dispatch-T4-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-agmsg-upstream-sync-T19-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-asset-manifest-T15-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-audit-exec-channel-T33e-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-audit-pane-hardening-T32b-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-audit-pane-prompt-detect-T33j-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-audit-pane-visibility-T32-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-audit-profile-gpt6-sol-T48-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-audit-verdict-gate-T33b-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-builtin-git-auto-T1-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ccstatusline-ubuntu26-hang-T59-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ci-runner-label-pin-T58-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-claude-sandbox-T13-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-claude-sandbox-manifest-T39-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-codex-apparmor-userns-T30-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-codex-worktree-git-writable-T50-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-dependabot-verify-T8-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-docs-align-T1-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-env-converge-T10-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-formatter-hook-root-fix-T61-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-git-ignore-cc-writes-T56-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-herdr-agents-add-worker-T22-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-herdr-agents-seat-labels-T35-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-herdr-sheldon-T1-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-herdr-sheldon-T1-a02.md
masked 0 match(es) in .orchestration/acceptance/dot-herdr-worker-relaunch-T25-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-macos-brew-untrusted-taps-T57-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-macos-crit-pinned-install-T17-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-main-push-guard-revert-T60-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-mise-pin-test-sync-T53-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-mise-symlink-T3-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-mosh-and-asset-bumps-T31-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-orchestration-hygiene-T33i-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-orchestration-rules-T33a-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-orchestration-rules-T43-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-orchestrator-delivery-sandbox-T49-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-orchestrator-linkage-evidence-T46-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-orchestrator-pane-profile-args-T47-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-permgate-bench-flake-T33d-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-permgate-codex-stdin-T33h-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-plain-start-visibility-T45-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-pr-feedback-gate-T16-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-pr-feedback-gate-T38-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-pr-gate-trust-boundary-T40-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-restart-worker-name-wait-T27-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-sandbox-unix-sockets-T44-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-security-profile-model-T42-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-three-role-constellation-T28-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-core-build-T33f-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-core-build-shim-T33g-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-full-T9-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-graph-refresh-T33c-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-graph-refresh-T36-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-graph-refresh-T41-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-graph-refresh-T51-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-graph-refresh-T55-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-refresh-T5-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ua-refresh-policy-T52-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-fix-T1-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T1-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T10-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T11-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T12-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T13-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T2-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T3-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T4-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T5-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T6-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T7-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T8-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-ubuntu-parity-T9-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-update-convergence-T1-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-upgrade-pin-path-codify-T54-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-upgrade-pins-T2-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-upgrade-pins-sync-T37-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-validator-worktrees-T7-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-version-currency-T29-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-worker-advisor-fable-T26-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-worker-kind-guard-T14-a01.md
masked 0 match(es) in .orchestration/acceptance/dot-worker-profile-opus55-T24-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T62-claude-auto-deny-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T63-codex-execpolicy-forbidden-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T64-codex-worker-never-network-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T65-agent-stop-gate-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T66-permgate-dead-lanes-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T67-audit-task-level-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T68-gate-audit-evidence-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T69-protocol-docs-unification-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T70-make-update-unattended-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T71-generator-multi-target-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T72-bootstrap-ci-pins-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T73-tool-versions-from-config-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T74-bootstrap-dead-code-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T75-shell-dead-code-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T76-ineffective-settings-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T77-harness-dead-code-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T77b-enforce-uv-hook-contract-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T78-dead-docs-adh-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T79-remove-adh-profile-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T80-codex-command-hooks-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T81-compactiondb-vendor-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T82-codex-compaction-hooks-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T83-docs-diet-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T84-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T85-launcher-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T86-codex-orchestrate-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T88-parallel-execution-rule-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T89-add-worker-same-workspace-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T90-github-identity-separation-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T90b-ruleset-sole-merger-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T91-secret-scan-sk-boundary-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T93-gate-masked-feedback-bodies-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T94-upgrade-pins-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T97-claude-sandbox-github-calls-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T98-evidence-home-path-masking-a01.md
masked 0 match(es) in .orchestration/acceptance/dotfiles-T99-nix-plans-history-a01.md
masked 0 match(es) in .orchestration/acceptance/fix-chezmoi-pycache-modify-exec.md
masked 0 match(es) in .orchestration/acceptance/plan-001.md
masked 0 match(es) in .orchestration/acceptance/plan-002.md
masked 0 match(es) in .orchestration/acceptance/plan-003-final-pr.md
masked 0 match(es) in .orchestration/acceptance/plan-003-review-round-1.md
masked 0 match(es) in .orchestration/acceptance/plan-003-review-round-2.md
masked 0 match(es) in .orchestration/acceptance/plan-003.md
masked 0 match(es) in .orchestration/acceptance/refkit-P0-01.md
masked 0 match(es) in .orchestration/acceptance/refkit-P0-05.md
masked 0 match(es) in .orchestration/acceptance/refkit-P0-06.md
masked 0 match(es) in .orchestration/acceptance/refkit-P0-07.md
masked 0 match(es) in .orchestration/acceptance/refkit-P1.md
masked 0 match(es) in .orchestration/acceptance/refkit-P2-A.md
masked 0 match(es) in .orchestration/acceptance/refkit-P2-B.md
masked 0 match(es) in .orchestration/acceptance/refkit-P2-C.md
masked 0 match(es) in .orchestration/acceptance/refkit-P3.md
masked 0 match(es) in .orchestration/acceptance/refkit-P4.md
masked 0 match(es) in .orchestration/acceptance/refkit-P5.md
masked 0 match(es) in .orchestration/acceptance/refkit-P7.md
masked 0 match(es) in .orchestration/acceptance/refkit-P8-a.md
masked 0 match(es) in .orchestration/acceptance/refkit-P8-b.md
masked 0 match(es) in .orchestration/acceptance/remote-diff-01.md
masked 0 match(es) in .orchestration/analysis/compactiondb-compaction-research.md
masked 0 match(es) in .orchestration/analysis/harness-composability-research.md
masked 0 match(es) in .orchestration/analysis/pi-harness-research.md
masked 0 match(es) in .orchestration/analysis/pi-pivot-decision.md
masked 0 match(es) in .orchestration/autoskill/runs/T10-herdr-files-pane.md
masked 0 match(es) in .orchestration/autoskill/runs/T11-agmsg-join-unique-identity-guard.md
masked 0 match(es) in .orchestration/autoskill/runs/T13-agmsg-orchestration-rule-file.md
masked 0 match(es) in .orchestration/autoskill/runs/T14-t13-pr-lifecycle.md
masked 0 match(es) in .orchestration/autoskill/runs/T15-herdr-lazy-start-attach-layout.md
masked 0 match(es) in .orchestration/autoskill/runs/T16-herdr-attach-layout-order-repair.md
masked 0 match(es) in .orchestration/autoskill/runs/T17-herdr-attach-agmsg-bootstrap.md
masked 0 match(es) in .orchestration/autoskill/runs/T18-herdr-agents-two-pane.md
masked 0 match(es) in .orchestration/autoskill/runs/T18-herdr-thirds-layout.md
masked 0 match(es) in .orchestration/autoskill/runs/T19-herdr-file-viewer-popup-config.md
masked 0 match(es) in .orchestration/autoskill/runs/T20-agmsg-setup-automation.md
masked 0 match(es) in .orchestration/autoskill/runs/T21-model-profiles-pr.md
masked 0 match(es) in .orchestration/autoskill/runs/T22-doctor-settings-idempotency.md
masked 0 match(es) in .orchestration/autoskill/runs/T23-agmsg-nudge-guidance.md
masked 0 match(es) in .orchestration/autoskill/runs/T24-usage-review-automation.md
masked 0 match(es) in .orchestration/autoskill/runs/T25-permgate-harness.md
masked 0 match(es) in .orchestration/autoskill/runs/T26-pr86-herdr-rebase.md
masked 0 match(es) in .orchestration/autoskill/runs/T27-pr87-npm-allow-scripts-rebase.md
masked 0 match(es) in .orchestration/autoskill/runs/T28-ccgate-removal-permgate-deploy.md
masked 0 match(es) in .orchestration/autoskill/runs/T29-agmsg-regime-default-on.md
masked 0 match(es) in .orchestration/autoskill/runs/T30-orchestration-evidence-sync.md
masked 0 match(es) in .orchestration/autoskill/runs/T31-codex-profile-modify-pattern.md
masked 0 match(es) in .orchestration/autoskill/runs/T32-evidence-and-mise-sync.md
masked 0 match(es) in .orchestration/autoskill/runs/T33-herdr-session-design-restore.md
masked 0 match(es) in .orchestration/autoskill/runs/T34-profile-codex-turn-delivery.md
masked 0 match(es) in .orchestration/autoskill/runs/T35-evidence-sync.md
masked 0 match(es) in .orchestration/autoskill/runs/T36-understand-anything-analysis.md
masked 0 match(es) in .orchestration/autoskill/runs/T37-understand-anything-codex-dist.md
masked 0 match(es) in .orchestration/autoskill/runs/T38-evidence-sync.md
masked 0 match(es) in .orchestration/autoskill/runs/T40-understand-anything-search-first.md
masked 0 match(es) in .orchestration/autoskill/runs/T41-remove-cognee.md
masked 0 match(es) in .orchestration/autoskill/runs/T42-zero-tail-evidence-sync.md
masked 0 match(es) in .orchestration/autoskill/runs/T43-compactiondb-integration.md
masked 0 match(es) in .orchestration/autoskill/runs/T44-marker-extraction-redesign.md
masked 0 match(es) in .orchestration/autoskill/runs/T45.md
masked 0 match(es) in .orchestration/autoskill/runs/T46.md
masked 0 match(es) in .orchestration/autoskill/runs/T47.md
masked 0 match(es) in .orchestration/autoskill/runs/T48.md
masked 0 match(es) in .orchestration/autoskill/runs/T48b.md
masked 0 match(es) in .orchestration/autoskill/runs/T48c.md
masked 0 match(es) in .orchestration/autoskill/runs/T49.md
masked 0 match(es) in .orchestration/autoskill/runs/T5.md
masked 0 match(es) in .orchestration/autoskill/runs/T50.md
masked 0 match(es) in .orchestration/autoskill/runs/T51a.md
masked 0 match(es) in .orchestration/autoskill/runs/T52.md
masked 0 match(es) in .orchestration/autoskill/runs/T53.md
masked 0 match(es) in .orchestration/autoskill/runs/T54.md
masked 0 match(es) in .orchestration/autoskill/runs/T55.md
masked 0 match(es) in .orchestration/autoskill/runs/T56.md
masked 0 match(es) in .orchestration/autoskill/runs/T56b.md
masked 0 match(es) in .orchestration/autoskill/runs/T57.md
masked 0 match(es) in .orchestration/autoskill/runs/T58.md
masked 0 match(es) in .orchestration/autoskill/runs/T59.md
masked 0 match(es) in .orchestration/autoskill/runs/T59b.md
masked 0 match(es) in .orchestration/autoskill/runs/T6.md
masked 0 match(es) in .orchestration/autoskill/runs/T60.md
masked 0 match(es) in .orchestration/autoskill/runs/T61a.md
masked 0 match(es) in .orchestration/autoskill/runs/T61b.md
masked 0 match(es) in .orchestration/autoskill/runs/T62.md
masked 0 match(es) in .orchestration/autoskill/runs/T62b.md
masked 0 match(es) in .orchestration/autoskill/runs/T62c.md
masked 0 match(es) in .orchestration/autoskill/runs/T63.md
masked 0 match(es) in .orchestration/autoskill/runs/T64.md
masked 0 match(es) in .orchestration/autoskill/runs/T64b.md
masked 0 match(es) in .orchestration/autoskill/runs/T65.md
masked 0 match(es) in .orchestration/autoskill/runs/T65b.md
masked 0 match(es) in .orchestration/autoskill/runs/T66.md
masked 0 match(es) in .orchestration/autoskill/runs/T66b.md
masked 0 match(es) in .orchestration/autoskill/runs/T66c.md
masked 0 match(es) in .orchestration/autoskill/runs/T66d.md
masked 0 match(es) in .orchestration/autoskill/runs/T66e.md
masked 0 match(es) in .orchestration/autoskill/runs/T67.md
masked 0 match(es) in .orchestration/autoskill/runs/T67b.md
masked 0 match(es) in .orchestration/autoskill/runs/T67c.md
masked 0 match(es) in .orchestration/autoskill/runs/T67d.md
masked 0 match(es) in .orchestration/autoskill/runs/T67e.md
masked 0 match(es) in .orchestration/autoskill/runs/T68.md
masked 0 match(es) in .orchestration/autoskill/runs/T68b.md
masked 0 match(es) in .orchestration/autoskill/runs/T68c.md
masked 0 match(es) in .orchestration/autoskill/runs/T69.md
masked 0 match(es) in .orchestration/autoskill/runs/T7.md
masked 0 match(es) in .orchestration/autoskill/runs/T70.md
masked 0 match(es) in .orchestration/autoskill/runs/T74.md
masked 0 match(es) in .orchestration/autoskill/runs/T76.md
masked 0 match(es) in .orchestration/autoskill/runs/T76b.md
masked 0 match(es) in .orchestration/autoskill/runs/T79-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T79b-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T8.md
masked 0 match(es) in .orchestration/autoskill/runs/T80-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T81-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T83-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T83b-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T84-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T84b-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T84c-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T85-autoskill.md
masked 0 match(es) in .orchestration/autoskill/runs/T86-herdr-agents-082-api-port.md
masked 0 match(es) in .orchestration/autoskill/runs/T87-boundary-bookkeeping-147.md
masked 0 match(es) in .orchestration/autoskill/runs/T9.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-A.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-B.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-C.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-D.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-E.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-F.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-G.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-H.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-I.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-J.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-K.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-L.md
masked 0 match(es) in .orchestration/autoskill/runs/WP-M.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-adh-baseline-T6-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-agent-assets-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-agmsg-dispatch-T4-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-agmsg-upstream-sync-T19-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-asset-manifest-T15-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-audit-exec-channel-T33e-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-audit-pane-hardening-T32b-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-audit-pane-prompt-detect-T33j-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-audit-pane-visibility-T32-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-audit-profile-gpt6-sol-T48-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-audit-verdict-gate-T33b-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-builtin-git-auto-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ccstatusline-ubuntu26-hang-T59-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ci-runner-label-pin-T58-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-claude-sandbox-manifest-T39-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-codex-apparmor-userns-T30-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-codex-worktree-git-writable-T50-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-crit-linux-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-dependabot-verify-T8-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-docs-align-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-env-converge-T10-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-formatter-hook-root-fix-T61-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-git-ignore-cc-writes-T56-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-herdr-agents-add-worker-T22-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-herdr-agents-seat-labels-T35-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-herdr-sheldon-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-herdr-sheldon-T1-a02.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-herdr-worker-relaunch-T25-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-macos-brew-untrusted-taps-T57-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-macos-crit-pinned-install-T17-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-main-push-guard-revert-T60-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-mise-pin-test-sync-T53-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-mise-symlink-T3-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-mkt-mode-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-mkt-owner-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-mosh-and-asset-bumps-T31-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-orchestration-hygiene-T33i-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-orchestration-rules-T33a-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-orchestration-rules-T43-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-orchestrator-delivery-sandbox-T49-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-orchestrator-linkage-evidence-T46-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-orchestrator-pane-profile-args-T47-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-permgate-bench-flake-T33d-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-permgate-codex-stdin-T33h-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-plain-start-visibility-T45-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-pr-feedback-gate-T38-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-pr-gate-trust-boundary-T40-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-residuals-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-restart-worker-name-wait-T27-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-sandbox-unix-sockets-T44-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-security-profile-model-T42-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-shell-sp-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-three-role-constellation-T28-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-core-build-T33f-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-core-build-shim-T33g-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-full-T9-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-graph-refresh-T33c-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-graph-refresh-T36-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-graph-refresh-T41-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-graph-refresh-T51-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-graph-refresh-T55-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-refresh-T5-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ua-refresh-policy-T52-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ubuntu-fix-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ubuntu-parity-T2-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ubuntu-parity-T3-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ubuntu-parity-T4-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ubuntu-parity-T5-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ubuntu-parity-T6-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ubuntu-parity-T7-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ubuntu-parity-T8-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-ubuntu-parity-T9-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-update-conv-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-update-convergence-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-upgrade-pin-path-codify-T54-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-upgrade-pins-T2-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-upgrade-pins-sync-T37-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-upgrade-regen-T1-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-validator-worktrees-T7-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-version-currency-T29-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-worker-advisor-fable-T26-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-worker-kind-guard-T14-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dot-worker-profile-opus55-T24-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T62-claude-auto-deny-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T63-codex-execpolicy-forbidden-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T64-codex-worker-never-network-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T65-agent-stop-gate-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T66-permgate-dead-lanes-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T67-audit-task-level-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T68-gate-audit-evidence-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T69-protocol-docs-unification-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T70-make-update-unattended-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T71-generator-multi-target-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T72-bootstrap-ci-pins-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T73-tool-versions-from-config-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T74-bootstrap-dead-code-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T75-shell-dead-code-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T76-ineffective-settings-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T77-harness-dead-code-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T77b-enforce-uv-hook-contract-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T78-dead-docs-adh-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T79-remove-adh-profile-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T80-codex-command-hooks-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T81-compactiondb-vendor-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T82-codex-compaction-hooks-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T83-docs-diet-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T84-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T85-launcher-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T86-codex-orchestrate-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T88-parallel-execution-rule-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T89-add-worker-same-workspace-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T90b-ruleset-sole-merger-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T91-secret-scan-sk-boundary-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T93-gate-masked-feedback-bodies-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T94-upgrade-pins-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T97-claude-sandbox-github-calls-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T98-evidence-home-path-masking-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/dotfiles-T99-nix-plans-history-a01.md
masked 0 match(es) in .orchestration/autoskill/runs/fix-chezmoi-pycache-modify-exec.md
masked 0 match(es) in .orchestration/autoskill/runs/plan-001.md
masked 0 match(es) in .orchestration/autoskill/runs/plan-002.md
masked 0 match(es) in .orchestration/autoskill/runs/plan-003.md
masked 0 match(es) in .orchestration/autoskill/runs/remote-diff-01.md
masked 0 match(es) in .orchestration/learning/ORCH-2026-08-05-regime-breach.md
masked 0 match(es) in .orchestration/learning/T10-herdr-files-pane.md
masked 0 match(es) in .orchestration/learning/T11-agmsg-join-unique-identity-guard.md
masked 0 match(es) in .orchestration/learning/T13-agmsg-orchestration-rule-file.md
masked 0 match(es) in .orchestration/learning/T14-t13-pr-lifecycle.md
masked 0 match(es) in .orchestration/learning/T15-herdr-lazy-start-attach-layout.md
masked 0 match(es) in .orchestration/learning/T16-herdr-attach-layout-order-repair.md
masked 0 match(es) in .orchestration/learning/T17-herdr-attach-agmsg-bootstrap.md
masked 0 match(es) in .orchestration/learning/T18-herdr-agents-two-pane.md
masked 0 match(es) in .orchestration/learning/T18-herdr-thirds-layout.md
masked 0 match(es) in .orchestration/learning/T19-herdr-file-viewer-popup-config.md
masked 0 match(es) in .orchestration/learning/T20-agmsg-setup-automation.md
masked 0 match(es) in .orchestration/learning/T21-model-profiles-pr.md
masked 0 match(es) in .orchestration/learning/T22-doctor-settings-idempotency.md
masked 0 match(es) in .orchestration/learning/T23-agmsg-nudge-guidance.md
masked 0 match(es) in .orchestration/learning/T24-usage-review-automation.md
masked 0 match(es) in .orchestration/learning/T25-permgate-harness.md
masked 0 match(es) in .orchestration/learning/T26-pr86-herdr-rebase.md
masked 0 match(es) in .orchestration/learning/T27-pr87-npm-allow-scripts-rebase.md
masked 0 match(es) in .orchestration/learning/T28-ccgate-removal-permgate-deploy.md
masked 0 match(es) in .orchestration/learning/T29-agmsg-regime-default-on.md
masked 0 match(es) in .orchestration/learning/T30-orchestration-evidence-sync.md
masked 0 match(es) in .orchestration/learning/T31-codex-profile-modify-pattern.md
masked 0 match(es) in .orchestration/learning/T32-evidence-and-mise-sync.md
masked 0 match(es) in .orchestration/learning/T33-herdr-session-design-restore.md
masked 0 match(es) in .orchestration/learning/T34-profile-codex-turn-delivery.md
masked 0 match(es) in .orchestration/learning/T35-evidence-sync.md
masked 0 match(es) in .orchestration/learning/T36-understand-anything-analysis.md
masked 0 match(es) in .orchestration/learning/T37-understand-anything-codex-dist.md
masked 0 match(es) in .orchestration/learning/T38-evidence-sync.md
masked 0 match(es) in .orchestration/learning/T40-understand-anything-search-first.md
masked 0 match(es) in .orchestration/learning/T41-remove-cognee.md
masked 0 match(es) in .orchestration/learning/T42-zero-tail-evidence-sync.md
masked 0 match(es) in .orchestration/learning/T43-compactiondb-integration.md
masked 0 match(es) in .orchestration/learning/T44-marker-extraction-redesign.md
masked 0 match(es) in .orchestration/learning/T45.md
masked 0 match(es) in .orchestration/learning/T46.md
masked 0 match(es) in .orchestration/learning/T47.md
masked 0 match(es) in .orchestration/learning/T48.md
masked 0 match(es) in .orchestration/learning/T48b.md
masked 0 match(es) in .orchestration/learning/T48c.md
masked 0 match(es) in .orchestration/learning/T49.md
masked 0 match(es) in .orchestration/learning/T5.md
masked 0 match(es) in .orchestration/learning/T50.md
masked 0 match(es) in .orchestration/learning/T51a.md
masked 0 match(es) in .orchestration/learning/T52.md
masked 0 match(es) in .orchestration/learning/T53.md
masked 0 match(es) in .orchestration/learning/T54.md
masked 0 match(es) in .orchestration/learning/T55.md
masked 0 match(es) in .orchestration/learning/T56.md
masked 0 match(es) in .orchestration/learning/T56b.md
masked 0 match(es) in .orchestration/learning/T57.md
masked 0 match(es) in .orchestration/learning/T58.md
masked 0 match(es) in .orchestration/learning/T59.md
masked 0 match(es) in .orchestration/learning/T59b.md
masked 0 match(es) in .orchestration/learning/T6.md
masked 0 match(es) in .orchestration/learning/T60.md
masked 0 match(es) in .orchestration/learning/T61a.md
masked 0 match(es) in .orchestration/learning/T61b.md
masked 0 match(es) in .orchestration/learning/T62.md
masked 0 match(es) in .orchestration/learning/T62b.md
masked 0 match(es) in .orchestration/learning/T62c.md
masked 0 match(es) in .orchestration/learning/T63.md
masked 0 match(es) in .orchestration/learning/T64.md
masked 0 match(es) in .orchestration/learning/T64b.md
masked 0 match(es) in .orchestration/learning/T65.md
masked 0 match(es) in .orchestration/learning/T65b.md
masked 0 match(es) in .orchestration/learning/T66.md
masked 0 match(es) in .orchestration/learning/T66b.md
masked 0 match(es) in .orchestration/learning/T66c.md
masked 0 match(es) in .orchestration/learning/T66d.md
masked 0 match(es) in .orchestration/learning/T66e.md
masked 0 match(es) in .orchestration/learning/T67.md
masked 0 match(es) in .orchestration/learning/T67b.md
masked 0 match(es) in .orchestration/learning/T67c.md
masked 0 match(es) in .orchestration/learning/T67d.md
masked 0 match(es) in .orchestration/learning/T67e.md
masked 0 match(es) in .orchestration/learning/T68.md
masked 0 match(es) in .orchestration/learning/T68b.md
masked 0 match(es) in .orchestration/learning/T68c.md
masked 0 match(es) in .orchestration/learning/T69.md
masked 0 match(es) in .orchestration/learning/T7.md
masked 0 match(es) in .orchestration/learning/T70.md
masked 0 match(es) in .orchestration/learning/T74.md
masked 0 match(es) in .orchestration/learning/T76.md
masked 0 match(es) in .orchestration/learning/T76b.md
masked 0 match(es) in .orchestration/learning/T79-learning.md
masked 0 match(es) in .orchestration/learning/T79b-learning.md
masked 0 match(es) in .orchestration/learning/T8.md
masked 0 match(es) in .orchestration/learning/T80-learning.md
masked 0 match(es) in .orchestration/learning/T81-learning.md
masked 0 match(es) in .orchestration/learning/T83-learning.md
masked 0 match(es) in .orchestration/learning/T83b-learning.md
masked 0 match(es) in .orchestration/learning/T84-learning.md
masked 0 match(es) in .orchestration/learning/T84b-learning.md
masked 0 match(es) in .orchestration/learning/T84c-learning.md
masked 0 match(es) in .orchestration/learning/T85-learning.md
masked 0 match(es) in .orchestration/learning/T86-herdr-agents-082-api-port.md
masked 0 match(es) in .orchestration/learning/T87-boundary-bookkeeping-147.md
masked 0 match(es) in .orchestration/learning/T9.md
masked 0 match(es) in .orchestration/learning/WP-A.md
masked 0 match(es) in .orchestration/learning/WP-B.md
masked 0 match(es) in .orchestration/learning/WP-C.md
masked 0 match(es) in .orchestration/learning/WP-D.md
masked 0 match(es) in .orchestration/learning/WP-E.md
masked 0 match(es) in .orchestration/learning/WP-F.md
masked 0 match(es) in .orchestration/learning/WP-G.md
masked 0 match(es) in .orchestration/learning/WP-H.md
masked 0 match(es) in .orchestration/learning/WP-I.md
masked 0 match(es) in .orchestration/learning/WP-J.md
masked 0 match(es) in .orchestration/learning/WP-K.md
masked 0 match(es) in .orchestration/learning/WP-L.md
masked 0 match(es) in .orchestration/learning/WP-M.md
masked 0 match(es) in .orchestration/learning/dot-adh-baseline-T6-a01.md
masked 0 match(es) in .orchestration/learning/dot-agent-assets-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-agmsg-dispatch-T4-a01.md
masked 0 match(es) in .orchestration/learning/dot-agmsg-upstream-sync-T19-a01.md
masked 0 match(es) in .orchestration/learning/dot-asset-manifest-T15-a01.md
masked 0 match(es) in .orchestration/learning/dot-audit-exec-channel-T33e-a01.md
masked 0 match(es) in .orchestration/learning/dot-audit-pane-hardening-T32b-a01.md
masked 0 match(es) in .orchestration/learning/dot-audit-pane-prompt-detect-T33j-a01.md
masked 0 match(es) in .orchestration/learning/dot-audit-pane-visibility-T32-a01.md
masked 0 match(es) in .orchestration/learning/dot-audit-profile-gpt6-sol-T48-a01.md
masked 0 match(es) in .orchestration/learning/dot-audit-verdict-gate-T33b-a01.md
masked 0 match(es) in .orchestration/learning/dot-builtin-git-auto-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-ccstatusline-ubuntu26-hang-T59-a01.md
masked 0 match(es) in .orchestration/learning/dot-ci-runner-label-pin-T58-a01.md
masked 0 match(es) in .orchestration/learning/dot-claude-sandbox-manifest-T39-a01.md
masked 0 match(es) in .orchestration/learning/dot-codex-apparmor-userns-T30-a01.md
masked 0 match(es) in .orchestration/learning/dot-codex-worktree-git-writable-T50-a01.md
masked 0 match(es) in .orchestration/learning/dot-crit-linux-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-dependabot-verify-T8-a01.md
masked 0 match(es) in .orchestration/learning/dot-docs-align-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-env-converge-T10-a01.md
masked 0 match(es) in .orchestration/learning/dot-formatter-hook-root-fix-T61-a01.md
masked 0 match(es) in .orchestration/learning/dot-git-ignore-cc-writes-T56-a01.md
masked 0 match(es) in .orchestration/learning/dot-herdr-agents-add-worker-T22-a01.md
masked 0 match(es) in .orchestration/learning/dot-herdr-agents-seat-labels-T35-a01.md
masked 0 match(es) in .orchestration/learning/dot-herdr-sheldon-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-herdr-sheldon-T1-a02.md
masked 0 match(es) in .orchestration/learning/dot-herdr-worker-relaunch-T25-a01.md
masked 0 match(es) in .orchestration/learning/dot-macos-brew-untrusted-taps-T57-a01.md
masked 0 match(es) in .orchestration/learning/dot-macos-crit-pinned-install-T17-a01.md
masked 0 match(es) in .orchestration/learning/dot-main-push-guard-revert-T60-a01.md
masked 0 match(es) in .orchestration/learning/dot-mise-pin-test-sync-T53-a01.md
masked 0 match(es) in .orchestration/learning/dot-mise-symlink-T3-a01.md
masked 0 match(es) in .orchestration/learning/dot-mkt-mode-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-mkt-owner-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-mosh-and-asset-bumps-T31-a01.md
masked 0 match(es) in .orchestration/learning/dot-orchestration-hygiene-T33i-a01.md
masked 0 match(es) in .orchestration/learning/dot-orchestration-rules-T33a-a01.md
masked 0 match(es) in .orchestration/learning/dot-orchestration-rules-T43-a01.md
masked 0 match(es) in .orchestration/learning/dot-orchestrator-delivery-sandbox-T49-a01.md
masked 0 match(es) in .orchestration/learning/dot-orchestrator-linkage-evidence-T46-a01.md
masked 0 match(es) in .orchestration/learning/dot-orchestrator-pane-profile-args-T47-a01.md
masked 0 match(es) in .orchestration/learning/dot-permgate-bench-flake-T33d-a01.md
masked 0 match(es) in .orchestration/learning/dot-permgate-codex-stdin-T33h-a01.md
masked 0 match(es) in .orchestration/learning/dot-plain-start-visibility-T45-a01.md
masked 0 match(es) in .orchestration/learning/dot-pr-feedback-gate-T38-a01.md
masked 0 match(es) in .orchestration/learning/dot-pr-gate-trust-boundary-T40-a01.md
masked 0 match(es) in .orchestration/learning/dot-residuals-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-restart-worker-name-wait-T27-a01.md
masked 0 match(es) in .orchestration/learning/dot-sandbox-unix-sockets-T44-a01.md
masked 0 match(es) in .orchestration/learning/dot-security-profile-model-T42-a01.md
masked 0 match(es) in .orchestration/learning/dot-shell-sp-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-three-role-constellation-T28-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-core-build-T33f-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-core-build-shim-T33g-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-full-T9-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-graph-refresh-T33c-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-graph-refresh-T36-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-graph-refresh-T41-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-graph-refresh-T51-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-graph-refresh-T55-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-refresh-T5-a01.md
masked 0 match(es) in .orchestration/learning/dot-ua-refresh-policy-T52-a01.md
masked 0 match(es) in .orchestration/learning/dot-ubuntu-fix-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-ubuntu-parity-T2-a01.md
masked 0 match(es) in .orchestration/learning/dot-ubuntu-parity-T3-a01.md
masked 0 match(es) in .orchestration/learning/dot-ubuntu-parity-T4-a01.md
masked 0 match(es) in .orchestration/learning/dot-ubuntu-parity-T5-a01.md
masked 0 match(es) in .orchestration/learning/dot-ubuntu-parity-T6-a01.md
masked 0 match(es) in .orchestration/learning/dot-ubuntu-parity-T7-a01.md
masked 0 match(es) in .orchestration/learning/dot-ubuntu-parity-T8-a01.md
masked 0 match(es) in .orchestration/learning/dot-ubuntu-parity-T9-a01.md
masked 0 match(es) in .orchestration/learning/dot-update-conv-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-update-convergence-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-upgrade-pin-path-codify-T54-a01.md
masked 0 match(es) in .orchestration/learning/dot-upgrade-pins-T2-a01.md
masked 0 match(es) in .orchestration/learning/dot-upgrade-pins-sync-T37-a01.md
masked 0 match(es) in .orchestration/learning/dot-upgrade-regen-T1-a01.md
masked 0 match(es) in .orchestration/learning/dot-validator-worktrees-T7-a01.md
masked 0 match(es) in .orchestration/learning/dot-version-currency-T29-a01.md
masked 0 match(es) in .orchestration/learning/dot-worker-advisor-fable-T26-a01.md
masked 0 match(es) in .orchestration/learning/dot-worker-kind-guard-T14-a01.md
masked 0 match(es) in .orchestration/learning/dot-worker-profile-opus55-T24-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T62-claude-auto-deny-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T63-codex-execpolicy-forbidden-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T64-codex-worker-never-network-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T65-agent-stop-gate-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T66-permgate-dead-lanes-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T67-audit-task-level-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T68-gate-audit-evidence-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T69-protocol-docs-unification-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T70-make-update-unattended-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T71-generator-multi-target-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T72-bootstrap-ci-pins-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T73-tool-versions-from-config-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T74-bootstrap-dead-code-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T75-shell-dead-code-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T76-ineffective-settings-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T77-harness-dead-code-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T77b-enforce-uv-hook-contract-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T78-dead-docs-adh-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T79-remove-adh-profile-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T80-codex-command-hooks-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T81-compactiondb-vendor-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T82-codex-compaction-hooks-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T83-docs-diet-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T84-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T85-launcher-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T86-codex-orchestrate-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T88-parallel-execution-rule-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T89-add-worker-same-workspace-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T90b-ruleset-sole-merger-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T91-secret-scan-sk-boundary-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T93-gate-masked-feedback-bodies-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T94-upgrade-pins-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T97-claude-sandbox-github-calls-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T98-evidence-home-path-masking-a01.md
masked 0 match(es) in .orchestration/learning/dotfiles-T99-nix-plans-history-a01.md
masked 0 match(es) in .orchestration/learning/fix-chezmoi-pycache-modify-exec.md
masked 0 match(es) in .orchestration/learning/plan-001.md
masked 0 match(es) in .orchestration/learning/plan-002.md
masked 0 match(es) in .orchestration/learning/plan-003.md
masked 0 match(es) in .orchestration/learning/plan-004.md
masked 0 match(es) in .orchestration/learning/remote-diff-01.md
masked 0 match(es) in .orchestration/learning/rule_candidates/agmsg-worker-identity-delivery.md
masked 0 match(es) in .orchestration/learning/rule_candidates/audit-evidence-secret-validator.md
masked 0 match(es) in .orchestration/learning/rule_candidates/herdr-worker-relaunch.md
masked 0 match(es) in .orchestration/learning/rule_candidates/ua-hook-out-of-scope-for-workers.md
masked 0 match(es) in .orchestration/learning/rule_candidates/understand-anything-core-build.md
masked 0 match(es) in .orchestration/reports/P0-04-sources.md
masked 0 match(es) in .orchestration/reports/T10-herdr-files-pane.md
masked 0 match(es) in .orchestration/reports/T11-agmsg-join-unique-identity-guard.md
masked 0 match(es) in .orchestration/reports/T13-agmsg-orchestration-rule-file.md
masked 0 match(es) in .orchestration/reports/T14-t13-pr-lifecycle.md
masked 0 match(es) in .orchestration/reports/T15-herdr-lazy-start-attach-layout.md
masked 0 match(es) in .orchestration/reports/T16-herdr-attach-layout-order-repair.md
masked 0 match(es) in .orchestration/reports/T17-herdr-attach-agmsg-bootstrap.md
masked 0 match(es) in .orchestration/reports/T18-herdr-agents-two-pane.md
masked 0 match(es) in .orchestration/reports/T18-herdr-thirds-layout.md
masked 0 match(es) in .orchestration/reports/T18-pr76-review-fixes.md
masked 0 match(es) in .orchestration/reports/T19-bootstrap-home-guard.md
masked 0 match(es) in .orchestration/reports/T19-herdr-file-viewer-popup-config.md
masked 0 match(es) in .orchestration/reports/T20-agmsg-setup-automation.md
masked 0 match(es) in .orchestration/reports/T21-model-profiles-pr.md
masked 0 match(es) in .orchestration/reports/T22-doctor-settings-idempotency.md
masked 0 match(es) in .orchestration/reports/T23-agmsg-nudge-guidance.md
masked 0 match(es) in .orchestration/reports/T24-usage-review-automation.md
masked 0 match(es) in .orchestration/reports/T25-permgate-harness.md
masked 0 match(es) in .orchestration/reports/T26-pr86-herdr-rebase.md
masked 0 match(es) in .orchestration/reports/T27-pr87-npm-allow-scripts-rebase.md
masked 0 match(es) in .orchestration/reports/T28-ccgate-removal-permgate-deploy.md
masked 0 match(es) in .orchestration/reports/T29-agmsg-regime-default-on.md
masked 0 match(es) in .orchestration/reports/T30-orchestration-evidence-sync.md
masked 0 match(es) in .orchestration/reports/T31-codex-profile-modify-pattern.md
masked 0 match(es) in .orchestration/reports/T32-evidence-and-mise-sync.md
masked 0 match(es) in .orchestration/reports/T33-herdr-session-design-restore.md
masked 0 match(es) in .orchestration/reports/T34-profile-codex-turn-delivery.md
masked 0 match(es) in .orchestration/reports/T35-evidence-sync.md
masked 0 match(es) in .orchestration/reports/T36-understand-anything-analysis.md
masked 0 match(es) in .orchestration/reports/T37-understand-anything-codex-dist.md
masked 0 match(es) in .orchestration/reports/T38-evidence-sync.md
masked 0 match(es) in .orchestration/reports/T40-understand-anything-search-first.md
masked 0 match(es) in .orchestration/reports/T41-remove-cognee.md
masked 0 match(es) in .orchestration/reports/T42-zero-tail-evidence-sync.md
masked 0 match(es) in .orchestration/reports/T43-compactiondb-integration.md
masked 0 match(es) in .orchestration/reports/T44-marker-extraction-redesign.md
masked 0 match(es) in .orchestration/reports/T45.md
masked 0 match(es) in .orchestration/reports/T46.md
masked 0 match(es) in .orchestration/reports/T47.md
masked 0 match(es) in .orchestration/reports/T48.md
masked 0 match(es) in .orchestration/reports/T48b.md
masked 0 match(es) in .orchestration/reports/T48c.md
masked 0 match(es) in .orchestration/reports/T49.md
masked 0 match(es) in .orchestration/reports/T5.md
masked 0 match(es) in .orchestration/reports/T50.md
masked 0 match(es) in .orchestration/reports/T51a.md
masked 0 match(es) in .orchestration/reports/T52.md
masked 0 match(es) in .orchestration/reports/T53.md
masked 0 match(es) in .orchestration/reports/T54.md
masked 0 match(es) in .orchestration/reports/T55.md
masked 0 match(es) in .orchestration/reports/T56.md
masked 0 match(es) in .orchestration/reports/T56b.md
masked 0 match(es) in .orchestration/reports/T57.md
masked 0 match(es) in .orchestration/reports/T58.md
masked 0 match(es) in .orchestration/reports/T59.md
masked 0 match(es) in .orchestration/reports/T59b.md
masked 0 match(es) in .orchestration/reports/T6.md
masked 0 match(es) in .orchestration/reports/T60.md
masked 0 match(es) in .orchestration/reports/T61a.md
masked 0 match(es) in .orchestration/reports/T61b.md
masked 0 match(es) in .orchestration/reports/T62.md
masked 0 match(es) in .orchestration/reports/T62b.md
masked 0 match(es) in .orchestration/reports/T62c.md
masked 0 match(es) in .orchestration/reports/T63.md
masked 0 match(es) in .orchestration/reports/T64.md
masked 0 match(es) in .orchestration/reports/T64b.md
masked 0 match(es) in .orchestration/reports/T65.md
masked 0 match(es) in .orchestration/reports/T65b.md
masked 0 match(es) in .orchestration/reports/T66.md
masked 0 match(es) in .orchestration/reports/T66b.md
masked 0 match(es) in .orchestration/reports/T66c.md
masked 0 match(es) in .orchestration/reports/T66d.md
masked 0 match(es) in .orchestration/reports/T66e.md
masked 0 match(es) in .orchestration/reports/T67.md
masked 0 match(es) in .orchestration/reports/T67b.md
masked 0 match(es) in .orchestration/reports/T67c.md
masked 0 match(es) in .orchestration/reports/T67d.md
masked 0 match(es) in .orchestration/reports/T67e.md
masked 0 match(es) in .orchestration/reports/T68.md
masked 0 match(es) in .orchestration/reports/T68b.md
masked 0 match(es) in .orchestration/reports/T68c.md
masked 0 match(es) in .orchestration/reports/T69.md
masked 0 match(es) in .orchestration/reports/T7.md
masked 0 match(es) in .orchestration/reports/T70.md
masked 0 match(es) in .orchestration/reports/T74.md
masked 0 match(es) in .orchestration/reports/T76.md
masked 0 match(es) in .orchestration/reports/T76b.md
masked 0 match(es) in .orchestration/reports/T79-report.md
masked 0 match(es) in .orchestration/reports/T79b-report.md
masked 0 match(es) in .orchestration/reports/T8.md
masked 0 match(es) in .orchestration/reports/T80-report.md
masked 0 match(es) in .orchestration/reports/T81-report.md
masked 0 match(es) in .orchestration/reports/T83-report.md
masked 0 match(es) in .orchestration/reports/T83b-report.md
masked 0 match(es) in .orchestration/reports/T84-report.md
masked 0 match(es) in .orchestration/reports/T84b-report.md
masked 0 match(es) in .orchestration/reports/T84c-report.md
masked 0 match(es) in .orchestration/reports/T85-report.md
masked 0 match(es) in .orchestration/reports/T86-herdr-agents-082-api-port.md
masked 0 match(es) in .orchestration/reports/T87-boundary-bookkeeping-147.md
masked 0 match(es) in .orchestration/reports/T9.md
masked 0 match(es) in .orchestration/reports/WP-A.md
masked 0 match(es) in .orchestration/reports/WP-B.md
masked 0 match(es) in .orchestration/reports/WP-C.md
masked 0 match(es) in .orchestration/reports/WP-D.md
masked 0 match(es) in .orchestration/reports/WP-E.md
masked 0 match(es) in .orchestration/reports/WP-F.md
masked 0 match(es) in .orchestration/reports/WP-G.md
masked 0 match(es) in .orchestration/reports/WP-H.md
masked 0 match(es) in .orchestration/reports/WP-I.md
masked 0 match(es) in .orchestration/reports/WP-J.md
masked 0 match(es) in .orchestration/reports/WP-K.md
masked 0 match(es) in .orchestration/reports/WP-L.md
masked 0 match(es) in .orchestration/reports/WP-M.md
masked 0 match(es) in .orchestration/reports/dot-adh-baseline-T6-a01.md
masked 0 match(es) in .orchestration/reports/dot-agent-assets-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-agmsg-dispatch-T4-a01.md
masked 0 match(es) in .orchestration/reports/dot-agmsg-upstream-sync-T19-a01.md
masked 0 match(es) in .orchestration/reports/dot-asset-manifest-T15-a01.md
masked 0 match(es) in .orchestration/reports/dot-audit-exec-channel-T33e-a01.md
masked 0 match(es) in .orchestration/reports/dot-audit-pane-hardening-T32b-a01.md
masked 0 match(es) in .orchestration/reports/dot-audit-pane-prompt-detect-T33j-a01.md
masked 0 match(es) in .orchestration/reports/dot-audit-pane-visibility-T32-a01.md
masked 0 match(es) in .orchestration/reports/dot-audit-profile-gpt6-sol-T48-a01.md
masked 0 match(es) in .orchestration/reports/dot-audit-verdict-gate-T33b-a01.md
masked 0 match(es) in .orchestration/reports/dot-builtin-git-auto-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-ccstatusline-ubuntu26-hang-T59-a01.md
masked 0 match(es) in .orchestration/reports/dot-ci-runner-label-pin-T58-a01.md
masked 0 match(es) in .orchestration/reports/dot-claude-sandbox-T13-a01.md
masked 0 match(es) in .orchestration/reports/dot-claude-sandbox-manifest-T39-a01.md
masked 0 match(es) in .orchestration/reports/dot-codex-apparmor-userns-T30-a01.md
masked 0 match(es) in .orchestration/reports/dot-codex-worktree-git-writable-T50-a01.md
masked 0 match(es) in .orchestration/reports/dot-crit-linux-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-dependabot-verify-T8-a01.md
masked 0 match(es) in .orchestration/reports/dot-docs-align-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-env-converge-T10-a01.md
masked 0 match(es) in .orchestration/reports/dot-formatter-hook-root-fix-T61-a01.md
masked 0 match(es) in .orchestration/reports/dot-git-ignore-cc-writes-T56-a01.md
masked 0 match(es) in .orchestration/reports/dot-herdr-agents-add-worker-T22-a01.md
masked 0 match(es) in .orchestration/reports/dot-herdr-agents-seat-labels-T35-a01.md
masked 0 match(es) in .orchestration/reports/dot-herdr-sheldon-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-herdr-sheldon-T1-a02.md
masked 0 match(es) in .orchestration/reports/dot-herdr-worker-relaunch-T25-a01.md
masked 0 match(es) in .orchestration/reports/dot-macos-brew-untrusted-taps-T57-a01.md
masked 0 match(es) in .orchestration/reports/dot-macos-crit-pinned-install-T17-a01.md
masked 0 match(es) in .orchestration/reports/dot-main-push-guard-revert-T60-a01.md
masked 0 match(es) in .orchestration/reports/dot-mise-pin-test-sync-T53-a01.md
masked 0 match(es) in .orchestration/reports/dot-mise-symlink-T3-a01.md
masked 0 match(es) in .orchestration/reports/dot-mkt-mode-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-mkt-owner-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-mosh-and-asset-bumps-T31-a01.md
masked 0 match(es) in .orchestration/reports/dot-orchestration-hygiene-T33i-a01.md
masked 0 match(es) in .orchestration/reports/dot-orchestration-rules-T33a-a01.md
masked 0 match(es) in .orchestration/reports/dot-orchestration-rules-T43-a01.md
masked 0 match(es) in .orchestration/reports/dot-orchestrator-delivery-sandbox-T49-a01.md
masked 0 match(es) in .orchestration/reports/dot-orchestrator-linkage-evidence-T46-a01.md
masked 0 match(es) in .orchestration/reports/dot-orchestrator-pane-profile-args-T47-a01.md
masked 0 match(es) in .orchestration/reports/dot-permgate-bench-flake-T33d-a01.md
masked 0 match(es) in .orchestration/reports/dot-permgate-codex-stdin-T33h-a01.md
masked 0 match(es) in .orchestration/reports/dot-plain-start-visibility-T45-a01.md
masked 0 match(es) in .orchestration/reports/dot-pr-feedback-gate-T38-a01.md
masked 0 match(es) in .orchestration/reports/dot-pr-gate-trust-boundary-T40-a01.md
masked 0 match(es) in .orchestration/reports/dot-residuals-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-restart-worker-name-wait-T27-a01.md
masked 0 match(es) in .orchestration/reports/dot-sandbox-unix-sockets-T44-a01.md
masked 0 match(es) in .orchestration/reports/dot-security-profile-model-T42-a01.md
masked 0 match(es) in .orchestration/reports/dot-shell-sp-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-three-role-constellation-T28-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-core-build-T33f-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-core-build-shim-T33g-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-full-T9-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-graph-refresh-T33c-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-graph-refresh-T36-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-graph-refresh-T41-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-graph-refresh-T51-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-graph-refresh-T55-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-refresh-T5-a01.md
masked 0 match(es) in .orchestration/reports/dot-ua-refresh-policy-T52-a01.md
masked 0 match(es) in .orchestration/reports/dot-ubuntu-fix-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-ubuntu-parity-T2-a01.md
masked 0 match(es) in .orchestration/reports/dot-ubuntu-parity-T3-a01.md
masked 0 match(es) in .orchestration/reports/dot-ubuntu-parity-T4-a01.md
masked 0 match(es) in .orchestration/reports/dot-ubuntu-parity-T5-a01.md
masked 0 match(es) in .orchestration/reports/dot-ubuntu-parity-T6-a01.md
masked 0 match(es) in .orchestration/reports/dot-ubuntu-parity-T7-a01.md
masked 0 match(es) in .orchestration/reports/dot-ubuntu-parity-T8-a01.md
masked 0 match(es) in .orchestration/reports/dot-ubuntu-parity-T9-a01.md
masked 0 match(es) in .orchestration/reports/dot-update-conv-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-update-convergence-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-upgrade-pin-path-codify-T54-a01.md
masked 0 match(es) in .orchestration/reports/dot-upgrade-pins-T2-a01.md
masked 0 match(es) in .orchestration/reports/dot-upgrade-pins-sync-T37-a01.md
masked 0 match(es) in .orchestration/reports/dot-upgrade-regen-T1-a01.md
masked 0 match(es) in .orchestration/reports/dot-validator-worktrees-T7-a01.md
masked 0 match(es) in .orchestration/reports/dot-version-currency-T29-a01.md
masked 0 match(es) in .orchestration/reports/dot-worker-advisor-fable-T26-a01.md
masked 0 match(es) in .orchestration/reports/dot-worker-kind-guard-T14-a01.md
masked 0 match(es) in .orchestration/reports/dot-worker-profile-opus55-T24-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T62-claude-auto-deny-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T63-codex-execpolicy-forbidden-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T64-codex-worker-never-network-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T65-agent-stop-gate-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T66-permgate-dead-lanes-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T67-audit-task-level-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T68-gate-audit-evidence-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T69-protocol-docs-unification-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T70-make-update-unattended-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T71-generator-multi-target-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T72-bootstrap-ci-pins-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T73-tool-versions-from-config-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T74-bootstrap-dead-code-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T75-shell-dead-code-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T76-ineffective-settings-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T77-harness-dead-code-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T77b-enforce-uv-hook-contract-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T78-dead-docs-adh-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T79-remove-adh-profile-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T80-codex-command-hooks-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T81-compactiondb-vendor-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T82-codex-compaction-hooks-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T83-docs-diet-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T84-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T85-launcher-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T86-codex-orchestrate-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T88-parallel-execution-rule-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T89-add-worker-same-workspace-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T90b-ruleset-sole-merger-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T91-secret-scan-sk-boundary-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T93-gate-masked-feedback-bodies-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T94-upgrade-pins-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T97-claude-sandbox-github-calls-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T98-evidence-home-path-masking-a01.md
masked 0 match(es) in .orchestration/reports/dotfiles-T99-nix-plans-history-a01.md
masked 0 match(es) in .orchestration/reports/fix-chezmoi-pycache-modify-exec.md
masked 0 match(es) in .orchestration/reports/permgate-shadow-review-2026-07-24.md
masked 0 match(es) in .orchestration/reports/plan-001.md
masked 0 match(es) in .orchestration/reports/plan-002.md
masked 0 match(es) in .orchestration/reports/plan-003.md
masked 0 match(es) in .orchestration/reports/plan-004-inventory.md
masked 0 match(es) in .orchestration/reports/plan-004-stop.md
masked 0 match(es) in .orchestration/reports/plan-004.md
masked 0 match(es) in .orchestration/reports/remote-diff-01.md
masked 0 match(es) in .orchestration/sandboxes/T10-herdr-files-pane.md
masked 0 match(es) in .orchestration/sandboxes/T11-agmsg-join-unique-identity-guard.md
masked 0 match(es) in .orchestration/sandboxes/T13-agmsg-orchestration-rule-file.md
masked 0 match(es) in .orchestration/sandboxes/T14-t13-pr-lifecycle.md
masked 0 match(es) in .orchestration/sandboxes/T15-herdr-lazy-start-attach-layout.md
masked 0 match(es) in .orchestration/sandboxes/T16-herdr-attach-layout-order-repair.md
masked 0 match(es) in .orchestration/sandboxes/T17-herdr-attach-agmsg-bootstrap.md
masked 0 match(es) in .orchestration/sandboxes/T18-herdr-agents-two-pane.md
masked 0 match(es) in .orchestration/sandboxes/T18-herdr-thirds-layout.md
masked 0 match(es) in .orchestration/sandboxes/T19-herdr-file-viewer-popup-config.md
masked 0 match(es) in .orchestration/sandboxes/T20-agmsg-setup-automation.md
masked 0 match(es) in .orchestration/sandboxes/T21-model-profiles-pr.md
masked 0 match(es) in .orchestration/sandboxes/T22-doctor-settings-idempotency.md
masked 0 match(es) in .orchestration/sandboxes/T23-agmsg-nudge-guidance.md
masked 0 match(es) in .orchestration/sandboxes/T24-usage-review-automation.md
masked 0 match(es) in .orchestration/sandboxes/T25-permgate-harness.md
masked 0 match(es) in .orchestration/sandboxes/T26-pr86-herdr-rebase.md
masked 0 match(es) in .orchestration/sandboxes/T27-pr87-npm-allow-scripts-rebase.md
masked 0 match(es) in .orchestration/sandboxes/T28-ccgate-removal-permgate-deploy.md
masked 0 match(es) in .orchestration/sandboxes/T29-agmsg-regime-default-on.md
masked 0 match(es) in .orchestration/sandboxes/T30-orchestration-evidence-sync.md
masked 0 match(es) in .orchestration/sandboxes/T31-codex-profile-modify-pattern.md
masked 0 match(es) in .orchestration/sandboxes/T32-evidence-and-mise-sync.md
masked 0 match(es) in .orchestration/sandboxes/T33-herdr-session-design-restore.md
masked 0 match(es) in .orchestration/sandboxes/T34-profile-codex-turn-delivery.md
masked 0 match(es) in .orchestration/sandboxes/T35-evidence-sync.md
masked 0 match(es) in .orchestration/sandboxes/T36-understand-anything-analysis.md
masked 0 match(es) in .orchestration/sandboxes/T37-understand-anything-codex-dist.md
masked 0 match(es) in .orchestration/sandboxes/T38-evidence-sync.md
masked 0 match(es) in .orchestration/sandboxes/T40-understand-anything-search-first.md
masked 0 match(es) in .orchestration/sandboxes/T41-remove-cognee.md
masked 0 match(es) in .orchestration/sandboxes/T42-zero-tail-evidence-sync.md
masked 0 match(es) in .orchestration/sandboxes/T43-compactiondb-integration.md
masked 0 match(es) in .orchestration/sandboxes/T44-marker-extraction-redesign.md
masked 0 match(es) in .orchestration/sandboxes/T45.md
masked 0 match(es) in .orchestration/sandboxes/T46.md
masked 0 match(es) in .orchestration/sandboxes/T47.md
masked 0 match(es) in .orchestration/sandboxes/T48.md
masked 0 match(es) in .orchestration/sandboxes/T48b.md
masked 0 match(es) in .orchestration/sandboxes/T48c.md
masked 0 match(es) in .orchestration/sandboxes/T49.md
masked 0 match(es) in .orchestration/sandboxes/T5.md
masked 0 match(es) in .orchestration/sandboxes/T50.md
masked 0 match(es) in .orchestration/sandboxes/T51a.md
masked 0 match(es) in .orchestration/sandboxes/T52.md
masked 0 match(es) in .orchestration/sandboxes/T53.md
masked 0 match(es) in .orchestration/sandboxes/T54.md
masked 0 match(es) in .orchestration/sandboxes/T55.md
masked 0 match(es) in .orchestration/sandboxes/T56.md
masked 0 match(es) in .orchestration/sandboxes/T56b.md
masked 0 match(es) in .orchestration/sandboxes/T57.md
masked 0 match(es) in .orchestration/sandboxes/T58.md
masked 0 match(es) in .orchestration/sandboxes/T59.md
masked 0 match(es) in .orchestration/sandboxes/T59b.md
masked 0 match(es) in .orchestration/sandboxes/T6.md
masked 0 match(es) in .orchestration/sandboxes/T60.md
masked 0 match(es) in .orchestration/sandboxes/T61a.md
masked 0 match(es) in .orchestration/sandboxes/T61b.md
masked 0 match(es) in .orchestration/sandboxes/T62.md
masked 0 match(es) in .orchestration/sandboxes/T62b.md
masked 0 match(es) in .orchestration/sandboxes/T62c.md
masked 0 match(es) in .orchestration/sandboxes/T63.md
masked 0 match(es) in .orchestration/sandboxes/T64.md
masked 0 match(es) in .orchestration/sandboxes/T64b.md
masked 0 match(es) in .orchestration/sandboxes/T65.md
masked 0 match(es) in .orchestration/sandboxes/T65b.md
masked 0 match(es) in .orchestration/sandboxes/T66.md
masked 0 match(es) in .orchestration/sandboxes/T66b.md
masked 0 match(es) in .orchestration/sandboxes/T66c.md
masked 0 match(es) in .orchestration/sandboxes/T66d.md
masked 0 match(es) in .orchestration/sandboxes/T66e.md
masked 0 match(es) in .orchestration/sandboxes/T67.md
masked 0 match(es) in .orchestration/sandboxes/T67b.md
masked 0 match(es) in .orchestration/sandboxes/T67c.md
masked 0 match(es) in .orchestration/sandboxes/T67d.md
masked 0 match(es) in .orchestration/sandboxes/T67e.md
masked 0 match(es) in .orchestration/sandboxes/T68.md
masked 0 match(es) in .orchestration/sandboxes/T68b.md
masked 0 match(es) in .orchestration/sandboxes/T68c.md
masked 0 match(es) in .orchestration/sandboxes/T69.md
masked 0 match(es) in .orchestration/sandboxes/T7.md
masked 0 match(es) in .orchestration/sandboxes/T70.md
masked 0 match(es) in .orchestration/sandboxes/T74.md
masked 0 match(es) in .orchestration/sandboxes/T76.md
masked 0 match(es) in .orchestration/sandboxes/T76b.md
masked 0 match(es) in .orchestration/sandboxes/T79-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T79b-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T8.md
masked 0 match(es) in .orchestration/sandboxes/T80-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T81-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T83-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T83b-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T84-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T84b-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T84c-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T85-sandbox.md
masked 0 match(es) in .orchestration/sandboxes/T86-herdr-agents-082-api-port.md
masked 0 match(es) in .orchestration/sandboxes/T87-boundary-bookkeeping-147.md
masked 0 match(es) in .orchestration/sandboxes/T9.md
masked 0 match(es) in .orchestration/sandboxes/WP-A.md
masked 0 match(es) in .orchestration/sandboxes/WP-B.md
masked 0 match(es) in .orchestration/sandboxes/WP-C.md
masked 0 match(es) in .orchestration/sandboxes/WP-D.md
masked 0 match(es) in .orchestration/sandboxes/WP-E.md
masked 0 match(es) in .orchestration/sandboxes/WP-F.md
masked 0 match(es) in .orchestration/sandboxes/WP-G.md
masked 0 match(es) in .orchestration/sandboxes/WP-H.md
masked 0 match(es) in .orchestration/sandboxes/WP-I.md
masked 0 match(es) in .orchestration/sandboxes/WP-J.md
masked 0 match(es) in .orchestration/sandboxes/WP-K.md
masked 0 match(es) in .orchestration/sandboxes/WP-L.md
masked 0 match(es) in .orchestration/sandboxes/WP-M.md
masked 0 match(es) in .orchestration/sandboxes/dot-adh-baseline-T6-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-agent-assets-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-agmsg-dispatch-T4-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-agmsg-upstream-sync-T19-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-asset-manifest-T15-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-audit-exec-channel-T33e-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-audit-pane-hardening-T32b-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-audit-pane-prompt-detect-T33j-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-audit-pane-visibility-T32-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-audit-profile-gpt6-sol-T48-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-audit-verdict-gate-T33b-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-builtin-git-auto-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ccstatusline-ubuntu26-hang-T59-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ci-runner-label-pin-T58-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-claude-sandbox-manifest-T39-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-codex-apparmor-userns-T30-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-codex-worktree-git-writable-T50-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-crit-linux-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-dependabot-verify-T8-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-docs-align-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-env-converge-T10-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-formatter-hook-root-fix-T61-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-git-ignore-cc-writes-T56-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-herdr-agents-add-worker-T22-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-herdr-agents-seat-labels-T35-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-herdr-sheldon-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-herdr-sheldon-T1-a02.md
masked 0 match(es) in .orchestration/sandboxes/dot-herdr-worker-relaunch-T25-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-macos-brew-untrusted-taps-T57-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-macos-crit-pinned-install-T17-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-main-push-guard-revert-T60-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-mise-pin-test-sync-T53-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-mise-symlink-T3-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-mkt-mode-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-mkt-owner-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-mosh-and-asset-bumps-T31-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-orchestration-hygiene-T33i-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-orchestration-rules-T33a-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-orchestration-rules-T43-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-orchestrator-delivery-sandbox-T49-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-orchestrator-linkage-evidence-T46-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-orchestrator-pane-profile-args-T47-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-permgate-bench-flake-T33d-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-permgate-codex-stdin-T33h-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-plain-start-visibility-T45-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-pr-feedback-gate-T38-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-pr-gate-trust-boundary-T40-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-residuals-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-restart-worker-name-wait-T27-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-sandbox-unix-sockets-T44-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-security-profile-model-T42-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-shell-sp-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-three-role-constellation-T28-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-core-build-T33f-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-core-build-shim-T33g-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-full-T9-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-graph-refresh-T33c-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-graph-refresh-T36-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-graph-refresh-T41-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-graph-refresh-T51-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-graph-refresh-T55-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-refresh-T5-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ua-refresh-policy-T52-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ubuntu-fix-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ubuntu-parity-T2-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ubuntu-parity-T3-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ubuntu-parity-T4-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ubuntu-parity-T5-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ubuntu-parity-T6-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ubuntu-parity-T7-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ubuntu-parity-T8-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-ubuntu-parity-T9-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-update-conv-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-update-convergence-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-upgrade-pin-path-codify-T54-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-upgrade-pins-T2-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-upgrade-pins-sync-T37-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-upgrade-regen-T1-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-validator-worktrees-T7-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-version-currency-T29-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-worker-advisor-fable-T26-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-worker-kind-guard-T14-a01.md
masked 0 match(es) in .orchestration/sandboxes/dot-worker-profile-opus55-T24-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T62-claude-auto-deny-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T63-codex-execpolicy-forbidden-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T64-codex-worker-never-network-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T65-agent-stop-gate-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T66-permgate-dead-lanes-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T67-audit-task-level-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T68-gate-audit-evidence-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T69-protocol-docs-unification-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T70-make-update-unattended-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T71-generator-multi-target-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T72-bootstrap-ci-pins-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T73-tool-versions-from-config-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T74-bootstrap-dead-code-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T75-shell-dead-code-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T76-ineffective-settings-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T77-harness-dead-code-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T77b-enforce-uv-hook-contract-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T78-dead-docs-adh-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T79-remove-adh-profile-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T80-codex-command-hooks-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T81-compactiondb-vendor-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T82-codex-compaction-hooks-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T83-docs-diet-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T84-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T85-launcher-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T86-codex-orchestrate-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T88-parallel-execution-rule-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T89-add-worker-same-workspace-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T90b-ruleset-sole-merger-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T91-secret-scan-sk-boundary-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T93-gate-masked-feedback-bodies-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T94-upgrade-pins-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T97-claude-sandbox-github-calls-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T98-evidence-home-path-masking-a01.md
masked 0 match(es) in .orchestration/sandboxes/dotfiles-T99-nix-plans-history-a01.md
masked 0 match(es) in .orchestration/sandboxes/fix-chezmoi-pycache-modify-exec.md
masked 0 match(es) in .orchestration/sandboxes/plan-001.md
masked 0 match(es) in .orchestration/sandboxes/plan-002.md
masked 0 match(es) in .orchestration/sandboxes/plan-003.md
masked 0 match(es) in .orchestration/sandboxes/plan-004.md
masked 0 match(es) in .orchestration/sandboxes/remote-diff-01.md
masked 0 match(es) in .orchestration/tasks/PLAN-compactiondb-research-integration.md
masked 0 match(es) in .orchestration/tasks/PLAN-harness-composability-integration.md
masked 0 match(es) in .orchestration/tasks/PLAN-pi-pivot.md
masked 0 match(es) in .orchestration/tasks/PLAN-pi-worker-integration.md
masked 0 match(es) in .orchestration/tasks/T1-herdr-agents-idempotency.md
masked 0 match(es) in .orchestration/tasks/T10-herdr-files-pane.md
masked 0 match(es) in .orchestration/tasks/T11-agmsg-join-unique-identity-guard.md
masked 0 match(es) in .orchestration/tasks/T13-agmsg-orchestration-rule-file.md
masked 0 match(es) in .orchestration/tasks/T14-t13-pr-lifecycle.md
masked 0 match(es) in .orchestration/tasks/T15-herdr-lazy-start-attach-layout.md
masked 0 match(es) in .orchestration/tasks/T16-herdr-attach-layout-order-repair.md
masked 0 match(es) in .orchestration/tasks/T17-herdr-attach-agmsg-bootstrap.md
masked 0 match(es) in .orchestration/tasks/T18-herdr-agents-two-pane.md
masked 0 match(es) in .orchestration/tasks/T18-herdr-thirds-layout.md
masked 0 match(es) in .orchestration/tasks/T19-herdr-file-viewer-popup-config.md
masked 0 match(es) in .orchestration/tasks/T2-ensure-herdr-integrations.md
masked 0 match(es) in .orchestration/tasks/T20-agmsg-setup-automation.md
masked 0 match(es) in .orchestration/tasks/T21-model-profiles-pr.md
masked 0 match(es) in .orchestration/tasks/T22-doctor-settings-idempotency.md
masked 0 match(es) in .orchestration/tasks/T23-agmsg-nudge-guidance.md
masked 0 match(es) in .orchestration/tasks/T24-usage-review-automation.md
masked 0 match(es) in .orchestration/tasks/T25-permgate-harness.md
masked 0 match(es) in .orchestration/tasks/T26-pr86-herdr-rebase.md
masked 0 match(es) in .orchestration/tasks/T27-pr87-npm-allow-scripts-rebase.md
masked 0 match(es) in .orchestration/tasks/T28-ccgate-removal-permgate-deploy.md
masked 0 match(es) in .orchestration/tasks/T29-agmsg-regime-default-on.md
masked 0 match(es) in .orchestration/tasks/T3-agent-config-herdr-hook.md
masked 0 match(es) in .orchestration/tasks/T30-orchestration-evidence-sync.md
masked 0 match(es) in .orchestration/tasks/T31-codex-profile-modify-pattern.md
masked 0 match(es) in .orchestration/tasks/T32-evidence-and-mise-sync.md
masked 0 match(es) in .orchestration/tasks/T33-herdr-session-design-restore.md
masked 0 match(es) in .orchestration/tasks/T34-profile-codex-turn-delivery.md
masked 0 match(es) in .orchestration/tasks/T35-evidence-sync.md
masked 0 match(es) in .orchestration/tasks/T36-understand-anything-analysis.md
masked 0 match(es) in .orchestration/tasks/T37-understand-anything-codex-dist.md
masked 0 match(es) in .orchestration/tasks/T38-evidence-sync.md
masked 0 match(es) in .orchestration/tasks/T39-herdr-pin-fix.md
masked 0 match(es) in .orchestration/tasks/T4-readme-herdr-section.md
masked 0 match(es) in .orchestration/tasks/T40-understand-anything-search-first.md
masked 0 match(es) in .orchestration/tasks/T41-remove-cognee.md
masked 0 match(es) in .orchestration/tasks/T42-zero-tail-evidence-sync.md
masked 0 match(es) in .orchestration/tasks/T43-compactiondb-integration.md
masked 0 match(es) in .orchestration/tasks/T44-marker-extraction-redesign.md
masked 0 match(es) in .orchestration/tasks/T45-acceptance-memory-consolidation-rules.md
masked 0 match(es) in .orchestration/tasks/T46-compactiondb-recovery-config.md
masked 0 match(es) in .orchestration/tasks/T47-recovery-packet-sections.md
masked 0 match(es) in .orchestration/tasks/T48-codex-notify-ingest.md
masked 0 match(es) in .orchestration/tasks/T48b-ingest-source-attribution.md
masked 0 match(es) in .orchestration/tasks/T48c-notify-path-render.md
masked 0 match(es) in .orchestration/tasks/T49-probe-subcommand.md
masked 0 match(es) in .orchestration/tasks/T5-herdr-session-bootstrap.md
masked 0 match(es) in .orchestration/tasks/T50-recall-subcommand.md
masked 0 match(es) in .orchestration/tasks/T51a-shfmt-drift-fix.md
masked 0 match(es) in .orchestration/tasks/T52-ua-graph-update.md
masked 0 match(es) in .orchestration/tasks/T53-compactiondb-optin-dotfiles.md
masked 0 match(es) in .orchestration/tasks/T54-recovery-injection-ledger.md
masked 0 match(es) in .orchestration/tasks/T55-hook-composition-validation.md
masked 0 match(es) in .orchestration/tasks/T56-session-staleness.md
masked 0 match(es) in .orchestration/tasks/T56b-staleness-baseline-fix.md
masked 0 match(es) in .orchestration/tasks/T57-asset-install-manifest.md
masked 0 match(es) in .orchestration/tasks/T58-remove-agent-asset.md
masked 0 match(es) in .orchestration/tasks/T59-doctor-repair.md
masked 0 match(es) in .orchestration/tasks/T59b-repair-gaps.md
masked 0 match(es) in .orchestration/tasks/T6-claude-settings-modify-merge.md
masked 0 match(es) in .orchestration/tasks/T60-agmsg-effects-contract.md
masked 0 match(es) in .orchestration/tasks/T61a-ci-fixes.md
masked 0 match(es) in .orchestration/tasks/T61b-bot-review-fixes.md
masked 0 match(es) in .orchestration/tasks/T62-ua-graph-update.md
masked 0 match(es) in .orchestration/tasks/T62b-ua-shell-sources.md
masked 0 match(es) in .orchestration/tasks/T62c-ua-compactiondb-node.md
masked 0 match(es) in .orchestration/tasks/T63-e2e-driver-model-rule.md
masked 0 match(es) in .orchestration/tasks/T64-security-profile.md
masked 0 match(es) in .orchestration/tasks/T64b-codex-security-guidance.md
masked 0 match(es) in .orchestration/tasks/T65-pi-install-base.md
masked 0 match(es) in .orchestration/tasks/T65b-repin-0841.md
masked 0 match(es) in .orchestration/tasks/T66-permgate-pi.md
masked 0 match(es) in .orchestration/tasks/T66b-workspace-write-policy.md
masked 0 match(es) in .orchestration/tasks/T66c-read-semantics.md
masked 0 match(es) in .orchestration/tasks/T66d-tilde-normalization.md
masked 0 match(es) in .orchestration/tasks/T66e-strict-realpath.md
masked 0 match(es) in .orchestration/tasks/T67-model-access.md
masked 0 match(es) in .orchestration/tasks/T67b-checker-subscription-lane.md
masked 0 match(es) in .orchestration/tasks/T67c-checker-lane-precedence.md
masked 0 match(es) in .orchestration/tasks/T67d-checker-reasoning-models.md
masked 0 match(es) in .orchestration/tasks/T67e-checker-error-diagnostics.md
masked 0 match(es) in .orchestration/tasks/T68-rpc-agmsg-bridge.md
masked 0 match(es) in .orchestration/tasks/T68b-agmsg-send-tool.md
masked 0 match(es) in .orchestration/tasks/T68c-security-review-fixes.md
masked 0 match(es) in .orchestration/tasks/T69-contextdb-pi-extension.md
masked 0 match(es) in .orchestration/tasks/T7-zprofile-path-noninteractive.md
masked 0 match(es) in .orchestration/tasks/T70-pi-session-evidence.md
masked 0 match(es) in .orchestration/tasks/T74-pi-source-removal.md
masked 0 match(es) in .orchestration/tasks/T76-absorption.md
masked 0 match(es) in .orchestration/tasks/T76b-registration-grammar.md
masked 0 match(es) in .orchestration/tasks/T79-rule-two-tier.md
masked 0 match(es) in .orchestration/tasks/T79b-scope-qualifier-audit.md
masked 0 match(es) in .orchestration/tasks/T8-check-agent-runtime-drift.md
masked 0 match(es) in .orchestration/tasks/T80-codex-agents-two-tier.md
masked 0 match(es) in .orchestration/tasks/T81-result-cost-reporting.md
masked 0 match(es) in .orchestration/tasks/T83-ua-graph-update.md
masked 0 match(es) in .orchestration/tasks/T83b-ua-freshness-and-edges.md
masked 0 match(es) in .orchestration/tasks/T84-chezmoi-drift-resolution.md
masked 0 match(es) in .orchestration/tasks/T84b-bashsource-under-include.md
masked 0 match(es) in .orchestration/tasks/T84c-bats-private-profile-paths.md
masked 0 match(es) in .orchestration/tasks/T85-ua-graph-update-140.md
masked 0 match(es) in .orchestration/tasks/T86-herdr-agents-082-api-port.md
masked 0 match(es) in .orchestration/tasks/T87-boundary-bookkeeping-147.md
masked 0 match(es) in .orchestration/tasks/T9-herdr-lr-layout-gpt56sol.md
masked 0 match(es) in .orchestration/tasks/WP-A.md
masked 0 match(es) in .orchestration/tasks/WP-B.md
masked 0 match(es) in .orchestration/tasks/WP-C.md
masked 0 match(es) in .orchestration/tasks/WP-D.md
masked 0 match(es) in .orchestration/tasks/WP-E.md
masked 0 match(es) in .orchestration/tasks/WP-F.md
masked 0 match(es) in .orchestration/tasks/WP-G.md
masked 0 match(es) in .orchestration/tasks/WP-H.md
masked 0 match(es) in .orchestration/tasks/WP-I.md
masked 0 match(es) in .orchestration/tasks/WP-J.md
masked 0 match(es) in .orchestration/tasks/WP-K.md
masked 0 match(es) in .orchestration/tasks/WP-L.md
masked 0 match(es) in .orchestration/tasks/WP-M.md
masked 0 match(es) in .orchestration/tasks/dot-adh-baseline-T6-a01.md
masked 0 match(es) in .orchestration/tasks/dot-agent-assets-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-agmsg-dispatch-T4-a01.md
masked 0 match(es) in .orchestration/tasks/dot-agmsg-upstream-sync-T19-a01.md
masked 0 match(es) in .orchestration/tasks/dot-asset-manifest-T15-a01.md
masked 0 match(es) in .orchestration/tasks/dot-audit-exec-channel-T33e-a01.md
masked 0 match(es) in .orchestration/tasks/dot-audit-pane-hardening-T32b-a01.md
masked 0 match(es) in .orchestration/tasks/dot-audit-pane-prompt-detect-T33j-a01.md
masked 0 match(es) in .orchestration/tasks/dot-audit-pane-visibility-T32-a01.md
masked 0 match(es) in .orchestration/tasks/dot-audit-profile-gpt6-sol-T48-a01.md
masked 0 match(es) in .orchestration/tasks/dot-audit-verdict-gate-T33b-a01.md
masked 0 match(es) in .orchestration/tasks/dot-builtin-git-auto-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ccstatusline-ubuntu26-hang-T59-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ci-runner-label-pin-T58-a01.md
masked 0 match(es) in .orchestration/tasks/dot-claude-sandbox-T13-a01.md
masked 0 match(es) in .orchestration/tasks/dot-claude-sandbox-manifest-T39-a01.md
masked 0 match(es) in .orchestration/tasks/dot-codex-apparmor-userns-T30-a01.md
masked 0 match(es) in .orchestration/tasks/dot-codex-worktree-git-writable-T50-a01.md
masked 0 match(es) in .orchestration/tasks/dot-crit-linux-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-dependabot-verify-T8-a01.md
masked 0 match(es) in .orchestration/tasks/dot-docs-align-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-env-converge-T10-a01.md
masked 0 match(es) in .orchestration/tasks/dot-formatter-hook-root-fix-T61-a01.md
masked 0 match(es) in .orchestration/tasks/dot-git-ignore-cc-writes-T56-a01.md
masked 0 match(es) in .orchestration/tasks/dot-herdr-agents-add-worker-T22-a01.md
masked 0 match(es) in .orchestration/tasks/dot-herdr-agents-seat-labels-T35-a01.md
masked 0 match(es) in .orchestration/tasks/dot-herdr-sheldon-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-herdr-sheldon-T1-a02.md
masked 0 match(es) in .orchestration/tasks/dot-herdr-worker-relaunch-T25-a01.md
masked 0 match(es) in .orchestration/tasks/dot-herdr-worker-worktree-T11-a01.md
masked 0 match(es) in .orchestration/tasks/dot-macos-brew-untrusted-taps-T57-a01.md
masked 0 match(es) in .orchestration/tasks/dot-macos-crit-pinned-install-T17-a01.md
masked 0 match(es) in .orchestration/tasks/dot-main-push-guard-revert-T60-a01.md
masked 0 match(es) in .orchestration/tasks/dot-mise-pin-test-sync-T53-a01.md
masked 0 match(es) in .orchestration/tasks/dot-mise-symlink-T3-a01.md
masked 0 match(es) in .orchestration/tasks/dot-mkt-mode-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-mkt-owner-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-mosh-and-asset-bumps-T31-a01.md
masked 0 match(es) in .orchestration/tasks/dot-orchestration-hygiene-T33i-a01.md
masked 0 match(es) in .orchestration/tasks/dot-orchestration-rules-T33a-a01.md
masked 0 match(es) in .orchestration/tasks/dot-orchestration-rules-T43-a01.md
masked 0 match(es) in .orchestration/tasks/dot-orchestrator-delivery-sandbox-T49-a01.md
masked 0 match(es) in .orchestration/tasks/dot-orchestrator-guardrails-T21-a01.md
masked 0 match(es) in .orchestration/tasks/dot-orchestrator-linkage-evidence-T46-a01.md
masked 0 match(es) in .orchestration/tasks/dot-orchestrator-pane-profile-args-T47-a01.md
masked 0 match(es) in .orchestration/tasks/dot-permgate-bench-flake-T33d-a01.md
masked 0 match(es) in .orchestration/tasks/dot-permgate-codex-stdin-T33h-a01.md
masked 0 match(es) in .orchestration/tasks/dot-plain-start-visibility-T45-a01.md
masked 0 match(es) in .orchestration/tasks/dot-pr-feedback-gate-T16-a01.md
masked 0 match(es) in .orchestration/tasks/dot-pr-feedback-gate-T38-a01.md
masked 0 match(es) in .orchestration/tasks/dot-pr-gate-trust-boundary-T40-a01.md
masked 0 match(es) in .orchestration/tasks/dot-residuals-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-restart-worker-name-wait-T27-a01.md
masked 0 match(es) in .orchestration/tasks/dot-runner-label-pin-T18-a01.md
masked 0 match(es) in .orchestration/tasks/dot-sandbox-unix-sockets-T44-a01.md
masked 0 match(es) in .orchestration/tasks/dot-security-profile-model-T42-a01.md
masked 0 match(es) in .orchestration/tasks/dot-shell-sp-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-task-contract-v2-T23-a01.md
masked 0 match(es) in .orchestration/tasks/dot-three-role-constellation-T28-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-core-build-T33f-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-core-build-shim-T33g-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-full-T9-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-graph-refresh-T33c-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-graph-refresh-T36-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-graph-refresh-T41-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-graph-refresh-T51-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-graph-refresh-T55-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-hook-regex-T12-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-incremental-T20-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-refresh-T5-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ua-refresh-policy-T52-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-fix-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T10-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T11-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T12-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T13-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T2-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T3-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T4-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T5-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T6-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T7-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T8-a01.md
masked 0 match(es) in .orchestration/tasks/dot-ubuntu-parity-T9-a01.md
masked 0 match(es) in .orchestration/tasks/dot-update-conv-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-update-convergence-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-upgrade-pin-path-codify-T54-a01.md
masked 0 match(es) in .orchestration/tasks/dot-upgrade-pins-T2-a01.md
masked 0 match(es) in .orchestration/tasks/dot-upgrade-pins-sync-T37-a01.md
masked 0 match(es) in .orchestration/tasks/dot-upgrade-regen-T1-a01.md
masked 0 match(es) in .orchestration/tasks/dot-validator-worktrees-T7-a01.md
masked 0 match(es) in .orchestration/tasks/dot-version-currency-T29-a01.md
masked 0 match(es) in .orchestration/tasks/dot-worker-advisor-fable-T26-a01.md
masked 0 match(es) in .orchestration/tasks/dot-worker-kind-guard-T14-a01.md
masked 0 match(es) in .orchestration/tasks/dot-worker-profile-opus55-T24-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T62-claude-auto-deny-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T63-codex-execpolicy-forbidden-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T64-codex-worker-never-network-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T65-agent-stop-gate-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T66-permgate-dead-lanes-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T67-audit-task-level-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T68-gate-audit-evidence-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T69-protocol-docs-unification-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T70-make-update-unattended-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T71-generator-multi-target-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T72-bootstrap-ci-pins-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T73-tool-versions-from-config-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T74-bootstrap-dead-code-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T75-shell-dead-code-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T76-ineffective-settings-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T77-harness-dead-code-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T77b-enforce-uv-hook-contract-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T78-dead-docs-adh-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T79-remove-adh-profile-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T80-codex-command-hooks-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T81-compactiondb-vendor-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T82-codex-compaction-hooks-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T83-docs-diet-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T84-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T85-launcher-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T86-codex-orchestrate-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T87-live-e2e-matrix-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T88-parallel-execution-rule-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T89-add-worker-same-workspace-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T90-github-identity-separation-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T90b-ruleset-sole-merger-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T91-secret-scan-sk-boundary-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T93-gate-masked-feedback-bodies-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T94-pending-pins.patch
masked 0 match(es) in .orchestration/tasks/dotfiles-T94-upgrade-pins-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T97-claude-sandbox-github-calls-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T98-evidence-home-path-masking-a01.md
masked 0 match(es) in .orchestration/tasks/dotfiles-T99-nix-plans-history-a01.md
masked 0 match(es) in .orchestration/tasks/fix-chezmoi-pycache-modify-exec.md
masked 0 match(es) in .orchestration/tasks/plan-001.md
masked 0 match(es) in .orchestration/tasks/plan-002.md
masked 0 match(es) in .orchestration/tasks/plan-003.md
masked 0 match(es) in .orchestration/tasks/refkit-P0-01.md
masked 0 match(es) in .orchestration/tasks/refkit-P0-05.md
masked 0 match(es) in .orchestration/tasks/refkit-P0-06.md
masked 0 match(es) in .orchestration/tasks/refkit-P0-07.md
masked 0 match(es) in .orchestration/tasks/refkit-P1.md
masked 0 match(es) in .orchestration/tasks/refkit-P10.md
masked 0 match(es) in .orchestration/tasks/refkit-P2-A.md
masked 0 match(es) in .orchestration/tasks/refkit-P2-B.md
masked 0 match(es) in .orchestration/tasks/refkit-P2-C.md
masked 0 match(es) in .orchestration/tasks/refkit-P3.md
masked 0 match(es) in .orchestration/tasks/refkit-P4.md
masked 0 match(es) in .orchestration/tasks/refkit-P4b.md
masked 0 match(es) in .orchestration/tasks/refkit-P5.md
masked 0 match(es) in .orchestration/tasks/refkit-P6.md
masked 0 match(es) in .orchestration/tasks/refkit-P7.md
masked 0 match(es) in .orchestration/tasks/refkit-P8-a.md
masked 0 match(es) in .orchestration/tasks/refkit-P8-b.md
masked 0 match(es) in .orchestration/tasks/refkit-P8.md
masked 0 match(es) in .orchestration/tasks/refkit-P9.md
masked 0 match(es) in .orchestration/validation/T10-herdr-files-pane.md
masked 0 match(es) in .orchestration/validation/T11-agmsg-join-unique-identity-guard.md
masked 0 match(es) in .orchestration/validation/T13-agmsg-orchestration-rule-file.md
masked 0 match(es) in .orchestration/validation/T14-t13-pr-lifecycle.md
masked 0 match(es) in .orchestration/validation/T15-V1-verify.md
masked 0 match(es) in .orchestration/validation/T15-herdr-lazy-start-attach-layout.md
masked 0 match(es) in .orchestration/validation/T16-herdr-attach-layout-order-repair.md
masked 0 match(es) in .orchestration/validation/T17-herdr-attach-agmsg-bootstrap.md
masked 0 match(es) in .orchestration/validation/T18-herdr-agents-two-pane.md
masked 0 match(es) in .orchestration/validation/T18-herdr-thirds-layout.md
masked 0 match(es) in .orchestration/validation/T19-herdr-file-viewer-popup-config.md
masked 0 match(es) in .orchestration/validation/T20-agmsg-setup-automation.md
masked 0 match(es) in .orchestration/validation/T21-final-integration.txt
masked 0 match(es) in .orchestration/validation/T21-model-profiles-pr.txt
masked 0 match(es) in .orchestration/validation/T22-doctor-settings-idempotency.txt
masked 0 match(es) in .orchestration/validation/T23-agmsg-nudge-guidance.txt
masked 0 match(es) in .orchestration/validation/T24-usage-review-automation.txt
masked 0 match(es) in .orchestration/validation/T25-permgate-harness.txt
masked 0 match(es) in .orchestration/validation/T26-pr86-herdr-rebase.txt
masked 0 match(es) in .orchestration/validation/T27-pr87-npm-allow-scripts-rebase.txt
masked 0 match(es) in .orchestration/validation/T28-ccgate-removal-permgate-deploy.txt
masked 0 match(es) in .orchestration/validation/T28-crit-comments.json
masked 0 match(es) in .orchestration/validation/T28-review-receipt.md
masked 0 match(es) in .orchestration/validation/T29-agmsg-regime-default-on.md
masked 0 match(es) in .orchestration/validation/T30-orchestration-evidence-sync.md
masked 0 match(es) in .orchestration/validation/T31-codex-profile-modify-pattern.md
masked 0 match(es) in .orchestration/validation/T32-evidence-and-mise-sync.md
masked 0 match(es) in .orchestration/validation/T33-herdr-session-design-restore.md
masked 0 match(es) in .orchestration/validation/T34-profile-codex-turn-delivery.md
masked 0 match(es) in .orchestration/validation/T35-evidence-sync.md
masked 0 match(es) in .orchestration/validation/T36-understand-anything-analysis.md
masked 0 match(es) in .orchestration/validation/T37-understand-anything-codex-dist-crit-comments.json
masked 0 match(es) in .orchestration/validation/T37-understand-anything-codex-dist-review-receipt.md
masked 0 match(es) in .orchestration/validation/T37-understand-anything-codex-dist.md
masked 0 match(es) in .orchestration/validation/T38-evidence-sync.md
masked 0 match(es) in .orchestration/validation/T40-understand-anything-search-first.md
masked 0 match(es) in .orchestration/validation/T41-remove-cognee.md
masked 0 match(es) in .orchestration/validation/T42-zero-tail-evidence-sync.md
masked 0 match(es) in .orchestration/validation/T43-compactiondb-integration.md
masked 0 match(es) in .orchestration/validation/T44-marker-extraction-redesign-crit-comments.json
masked 0 match(es) in .orchestration/validation/T44-marker-extraction-redesign.md
masked 0 match(es) in .orchestration/validation/T45.txt
masked 0 match(es) in .orchestration/validation/T46.txt
masked 0 match(es) in .orchestration/validation/T47.txt
masked 0 match(es) in .orchestration/validation/T48.txt
masked 0 match(es) in .orchestration/validation/T48b.txt
masked 0 match(es) in .orchestration/validation/T48c.txt
masked 0 match(es) in .orchestration/validation/T49.txt
masked 0 match(es) in .orchestration/validation/T5.txt
masked 0 match(es) in .orchestration/validation/T50.txt
masked 0 match(es) in .orchestration/validation/T51-e2e.txt
masked 0 match(es) in .orchestration/validation/T51a.txt
masked 0 match(es) in .orchestration/validation/T52.txt
masked 0 match(es) in .orchestration/validation/T53.txt
masked 0 match(es) in .orchestration/validation/T54.txt
masked 0 match(es) in .orchestration/validation/T55.txt
masked 0 match(es) in .orchestration/validation/T56.txt
masked 0 match(es) in .orchestration/validation/T56b-crit-comments.json
masked 0 match(es) in .orchestration/validation/T56b-crit-receipt.md
masked 0 match(es) in .orchestration/validation/T56b.txt
masked 0 match(es) in .orchestration/validation/T57.txt
masked 0 match(es) in .orchestration/validation/T58.txt
masked 0 match(es) in .orchestration/validation/T59.txt
masked 0 match(es) in .orchestration/validation/T59b-crit-comments.json
masked 0 match(es) in .orchestration/validation/T59b-crit-receipt.md
masked 0 match(es) in .orchestration/validation/T59b.txt
masked 0 match(es) in .orchestration/validation/T6.txt
masked 0 match(es) in .orchestration/validation/T60.txt
masked 0 match(es) in .orchestration/validation/T61-e2e.txt
masked 0 match(es) in .orchestration/validation/T61a-crit-comments.json
masked 0 match(es) in .orchestration/validation/T61a-crit-receipt.md
masked 0 match(es) in .orchestration/validation/T61a.txt
masked 0 match(es) in .orchestration/validation/T61b-crit-comments.json
masked 0 match(es) in .orchestration/validation/T61b-crit-receipt.md
masked 0 match(es) in .orchestration/validation/T61b.txt
masked 0 match(es) in .orchestration/validation/T62.txt
masked 0 match(es) in .orchestration/validation/T62b.txt
masked 0 match(es) in .orchestration/validation/T62c.txt
masked 0 match(es) in .orchestration/validation/T63.txt
masked 0 match(es) in .orchestration/validation/T64.txt
masked 0 match(es) in .orchestration/validation/T64b.txt
masked 0 match(es) in .orchestration/validation/T65.txt
masked 0 match(es) in .orchestration/validation/T65b-anchors.md
masked 0 match(es) in .orchestration/validation/T65b.txt
masked 0 match(es) in .orchestration/validation/T66.txt
masked 0 match(es) in .orchestration/validation/T66b.txt
masked 0 match(es) in .orchestration/validation/T66c.txt
masked 0 match(es) in .orchestration/validation/T66d.txt
masked 0 match(es) in .orchestration/validation/T66e.txt
masked 0 match(es) in .orchestration/validation/T67-model-access.md
masked 0 match(es) in .orchestration/validation/T67.txt
masked 0 match(es) in .orchestration/validation/T67b.txt
masked 0 match(es) in .orchestration/validation/T67c.txt
masked 0 match(es) in .orchestration/validation/T67d.txt
masked 0 match(es) in .orchestration/validation/T67e.txt
masked 0 match(es) in .orchestration/validation/T68.txt
masked 0 match(es) in .orchestration/validation/T68b.txt
masked 0 match(es) in .orchestration/validation/T68c.txt
masked 0 match(es) in .orchestration/validation/T69.txt
masked 0 match(es) in .orchestration/validation/T7.txt
masked 0 match(es) in .orchestration/validation/T70.txt
masked 0 match(es) in .orchestration/validation/T72-e2e.txt
masked 0 match(es) in .orchestration/validation/T74.txt
masked 0 match(es) in .orchestration/validation/T76.txt
masked 0 match(es) in .orchestration/validation/T76b.txt
masked 0 match(es) in .orchestration/validation/T77-context-diet.md
masked 0 match(es) in .orchestration/validation/T79-validation.md
masked 0 match(es) in .orchestration/validation/T79b-validation.md
masked 0 match(es) in .orchestration/validation/T8.txt
masked 0 match(es) in .orchestration/validation/T80-validation.md
masked 0 match(es) in .orchestration/validation/T81-validation.md
masked 0 match(es) in .orchestration/validation/T82-context-diet-effect.md
masked 0 match(es) in .orchestration/validation/T83-validation.md
masked 0 match(es) in .orchestration/validation/T83b-validation.md
masked 0 match(es) in .orchestration/validation/T84-validation.md
masked 0 match(es) in .orchestration/validation/T84b-validation.md
masked 0 match(es) in .orchestration/validation/T84c-validation.md
masked 0 match(es) in .orchestration/validation/T85-validation.md
masked 0 match(es) in .orchestration/validation/T86-herdr-agents-082-api-port.md
masked 0 match(es) in .orchestration/validation/T87-boundary-bookkeeping-147.md
masked 0 match(es) in .orchestration/validation/T9.txt
masked 0 match(es) in .orchestration/validation/WP-A.txt
masked 0 match(es) in .orchestration/validation/WP-B.txt
masked 0 match(es) in .orchestration/validation/WP-C.txt
masked 0 match(es) in .orchestration/validation/WP-D.txt
masked 0 match(es) in .orchestration/validation/WP-E.txt
masked 0 match(es) in .orchestration/validation/WP-F.txt
masked 0 match(es) in .orchestration/validation/WP-G.txt
masked 0 match(es) in .orchestration/validation/WP-H.txt
masked 0 match(es) in .orchestration/validation/WP-I.txt
masked 0 match(es) in .orchestration/validation/WP-J.txt
masked 0 match(es) in .orchestration/validation/WP-K.txt
masked 0 match(es) in .orchestration/validation/WP-L.txt
masked 0 match(es) in .orchestration/validation/WP-M.txt
masked 0 match(es) in .orchestration/validation/agmsg-parallel-rule-crit-comments.json
masked 0 match(es) in .orchestration/validation/agmsg-parallel-rule-review-receipt.md
masked 0 match(es) in .orchestration/validation/baseline-20260925.md
masked 0 match(es) in .orchestration/validation/dot-adh-baseline-T6-a01.md
masked 0 match(es) in .orchestration/validation/dot-agent-assets-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-agmsg-dispatch-T4-a01.md
masked 0 match(es) in .orchestration/validation/dot-agmsg-upstream-sync-T19-a01-audit-r2.md
masked 0 match(es) in .orchestration/validation/dot-agmsg-upstream-sync-T19-a01-audit-r2.md.last.md
masked 0 match(es) in .orchestration/validation/dot-agmsg-upstream-sync-T19-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-agmsg-upstream-sync-T19-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-agmsg-upstream-sync-T19-a01-round2-crit.json
masked 0 match(es) in .orchestration/validation/dot-agmsg-upstream-sync-T19-a01-round2-orchestrator-crit.json
masked 0 match(es) in .orchestration/validation/dot-agmsg-upstream-sync-T19-a01-round2-orchestrator-receipt.md
masked 0 match(es) in .orchestration/validation/dot-agmsg-upstream-sync-T19-a01-round2-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-agmsg-upstream-sync-T19-a01.md
masked 0 match(es) in .orchestration/validation/dot-asset-manifest-T15-a01.md
masked 0 match(es) in .orchestration/validation/dot-audit-exec-channel-T33e-a01-audit-rev2.md
masked 0 match(es) in .orchestration/validation/dot-audit-exec-channel-T33e-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-audit-exec-channel-T33e-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-audit-exec-channel-T33e-a01-live-e2e.md
masked 0 match(es) in .orchestration/validation/dot-audit-exec-channel-T33e-a01-live-e2e.md.last.md
masked 0 match(es) in .orchestration/validation/dot-audit-exec-channel-T33e-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-audit-exec-channel-T33e-a01.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-hardening-T32b-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-hardening-T32b-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-audit-pane-hardening-T32b-a01-live-e2e.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-hardening-T32b-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-hardening-T32b-a01.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-live-e2e-2.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-live-e2e-2.md.last.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-live-e2e.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-live-e2e.md.last.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-visibility-T32-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-visibility-T32-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-audit-pane-visibility-T32-a01-live-e2e.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-visibility-T32-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-audit-pane-visibility-T32-a01.md
masked 0 match(es) in .orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01-audit-81d720f.md
masked 0 match(es) in .orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01-audit-81d720f.md.last.md
masked 0 match(es) in .orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01-audit-8956c3d.md
masked 0 match(es) in .orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01-audit-8956c3d.md.last.md
masked 0 match(es) in .orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-audit-profile-gpt6-sol-T48-a01.md
masked 0 match(es) in .orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev2.md
masked 0 match(es) in .orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev3.md
masked 0 match(es) in .orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-audit-verdict-gate-T33b-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-audit-verdict-gate-T33b-a01-live-e2e.md
masked 0 match(es) in .orchestration/validation/dot-audit-verdict-gate-T33b-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-audit-verdict-gate-T33b-a01.md
masked 0 match(es) in .orchestration/validation/dot-builtin-git-auto-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01.md
masked 0 match(es) in .orchestration/validation/dot-ci-runner-label-pin-T58-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-ci-runner-label-pin-T58-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ci-runner-label-pin-T58-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-ci-runner-label-pin-T58-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-ci-runner-label-pin-T58-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-ci-runner-label-pin-T58-a01.md
masked 0 match(es) in .orchestration/validation/dot-claude-sandbox-T13-a01.md
masked 0 match(es) in .orchestration/validation/dot-claude-sandbox-manifest-T39-a01-audit-841e12b.md
masked 0 match(es) in .orchestration/validation/dot-claude-sandbox-manifest-T39-a01-audit-841e12b.md.last.md
masked 0 match(es) in .orchestration/validation/dot-claude-sandbox-manifest-T39-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-claude-sandbox-manifest-T39-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-claude-sandbox-manifest-T39-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-claude-sandbox-manifest-T39-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-claude-sandbox-manifest-T39-a01.md
masked 0 match(es) in .orchestration/validation/dot-codex-apparmor-userns-T30-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-codex-apparmor-userns-T30-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-codex-apparmor-userns-T30-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-codex-apparmor-userns-T30-a01.md
masked 0 match(es) in .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-5952ab8.md
masked 0 match(es) in .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-5952ab8.md.last.md
masked 0 match(es) in .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-e334af5.md
masked 0 match(es) in .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-e334af5.md.last.md
masked 0 match(es) in .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-codex-worktree-git-writable-T50-a01.md
masked 0 match(es) in .orchestration/validation/dot-crit-linux-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-dependabot-verify-T8-a01.md
masked 0 match(es) in .orchestration/validation/dot-docs-align-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-env-converge-T10-a01.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-0827371f.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-0827371f.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-45d44292.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-45d44292.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-57021632.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-57021632.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-74ade52f.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-74ade52f.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-772ff3c6.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-772ff3c6.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-7dff3a5c.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-7dff3a5c.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ae806f37.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ae806f37.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-b5084de5.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-b5084de5.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-bd9a7995.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-bd9a7995.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-e5648fa6.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-e5648fa6.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ff37f41d.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ff37f41d.md.last.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-formatter-hook-root-fix-T61-a01.md
masked 0 match(es) in .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-git-ignore-cc-writes-T56-a01.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r4.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r4.md.last.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r5.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r5.md.last.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md.last.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-r4-orchestrator-crit.json
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-r4-orchestrator-receipt.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-add-worker-T22-a01.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-audit-rev2.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-audit-rev2.md.last.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-live-e2e.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-live-e2e.md.last.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-orchestrator-crit.json
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-orchestrator-receipt.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01.md
masked 0 match(es) in .orchestration/validation/dot-herdr-sheldon-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-herdr-sheldon-T1-a02.md
masked 0 match(es) in .orchestration/validation/dot-herdr-worker-relaunch-T25-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-herdr-worker-relaunch-T25-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-herdr-worker-relaunch-T25-a01.md
masked 0 match(es) in .orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-audit-rev1.md
masked 0 match(es) in .orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-audit-rev1.md.last.md
masked 0 match(es) in .orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-macos-brew-untrusted-taps-T57-a01.md
masked 0 match(es) in .orchestration/validation/dot-macos-crit-pinned-install-T17-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-macos-crit-pinned-install-T17-a01.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-4445917b.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-4445917b.md.last.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-560df81b.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-560df81b.md.last.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-rev1.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-audit-rev1.md.last.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-main-push-guard-revert-T60-a01.md
masked 0 match(es) in .orchestration/validation/dot-mise-pin-test-sync-T53-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-mise-pin-test-sync-T53-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-mise-pin-test-sync-T53-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-mise-pin-test-sync-T53-a01.md
masked 0 match(es) in .orchestration/validation/dot-mise-symlink-T3-a01.md
masked 0 match(es) in .orchestration/validation/dot-mkt-mode-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-mkt-owner-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-mosh-and-asset-bumps-T31-a01.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-hygiene-T33i-a01-audit-rev2.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-hygiene-T33i-a01-audit-rev2.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-hygiene-T33i-a01-audit-rev3.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-hygiene-T33i-a01-audit-rev3.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-hygiene-T33i-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-hygiene-T33i-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-hygiene-T33i-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-orchestration-hygiene-T33i-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-hygiene-T33i-a01.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T33a-a01-audit-rev3.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T33a-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T33a-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T33a-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T33a-a01.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-12d3f80.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-12d3f80.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-1843dd1.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-1843dd1.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-1b6741b.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-1b6741b.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-6b53337.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-6b53337.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-72746d4.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-72746d4.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-85919df.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-85919df.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-99c1174.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-99c1174.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-afb2c9d.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-afb2c9d.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-c878b0d.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit-c878b0d.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-orchestration-rules-T43-a01.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-00268f1.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-00268f1.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-11d87f3.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-11d87f3.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-1fa2a48.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-1fa2a48.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-229896a.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-229896a.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-4452516.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-4452516.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-50ebfdc.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-50ebfdc.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-63d4e03.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-63d4e03.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-68ac54d.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-68ac54d.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-99d734b.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-99d734b.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-9b658a9.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-9b658a9.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-9dc4e53.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-9dc4e53.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-e4903a1.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-audit-e4903a1.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-delivery-sandbox-T49-a01.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-00573f3.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-00573f3.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-2721f0c.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-2721f0c.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-63c993b.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-63c993b.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-7d0c585.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-7d0c585.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-91cc85f.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-91cc85f.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-98ea49f.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-98ea49f.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-9e36e63.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-9e36e63.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-a71e78d.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-a71e78d.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b91f949.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b91f949.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-bec48d4.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-bec48d4.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-d806a3d.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-d806a3d.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-pane-profile-args-T47-a01-audit-7103797.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-pane-profile-args-T47-a01-audit-7103797.md.last.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-pane-profile-args-T47-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-orchestrator-pane-profile-args-T47-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-orchestrator-pane-profile-args-T47-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-orchestrator-pane-profile-args-T47-a01.md
masked 0 match(es) in .orchestration/validation/dot-permgate-bench-flake-T33d-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-permgate-bench-flake-T33d-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-permgate-bench-flake-T33d-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-permgate-bench-flake-T33d-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-permgate-bench-flake-T33d-a01.md
masked 0 match(es) in .orchestration/validation/dot-permgate-codex-stdin-T33h-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-permgate-codex-stdin-T33h-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-permgate-codex-stdin-T33h-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-permgate-codex-stdin-T33h-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-permgate-codex-stdin-T33h-a01.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-0a35010.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-0a35010.md.last.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-51f8bc7.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-51f8bc7.md.last.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-89e95e4.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-89e95e4.md.last.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-9eb3e43.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-9eb3e43.md.last.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-dfdfbe8.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-dfdfbe8.md.last.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-e6f350b.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-audit-e6f350b.md.last.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-plain-start-visibility-T45-a01.md
masked 0 match(es) in .orchestration/validation/dot-pr-feedback-gate-T38-a01-audit-fa934f7.md
masked 0 match(es) in .orchestration/validation/dot-pr-feedback-gate-T38-a01-audit-fa934f7.md.last.md
masked 0 match(es) in .orchestration/validation/dot-pr-feedback-gate-T38-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-pr-feedback-gate-T38-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-pr-feedback-gate-T38-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-pr-feedback-gate-T38-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-pr-feedback-gate-T38-a01.md
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-audit-0dfe823.md
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-audit-0dfe823.md.last.md
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-audit-10dfc10.md
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-audit-10dfc10.md.last.md
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-audit-c67ec77.md
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-audit-c67ec77.md.last.md
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-review.json
masked 0 match(es) in .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01.md
masked 0 match(es) in .orchestration/validation/dot-residuals-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-restart-worker-name-wait-T27-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-restart-worker-name-wait-T27-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-restart-worker-name-wait-T27-a01.md
masked 0 match(es) in .orchestration/validation/dot-sandbox-unix-sockets-T44-a01-audit-c2c1f62.md
masked 0 match(es) in .orchestration/validation/dot-sandbox-unix-sockets-T44-a01-audit-c2c1f62.md.last.md
masked 0 match(es) in .orchestration/validation/dot-sandbox-unix-sockets-T44-a01-audit-dcb8839.md
masked 0 match(es) in .orchestration/validation/dot-sandbox-unix-sockets-T44-a01-audit-dcb8839.md.last.md
masked 0 match(es) in .orchestration/validation/dot-sandbox-unix-sockets-T44-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-sandbox-unix-sockets-T44-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-sandbox-unix-sockets-T44-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-sandbox-unix-sockets-T44-a01.md
masked 0 match(es) in .orchestration/validation/dot-security-profile-model-T42-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-security-profile-model-T42-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-security-profile-model-T42-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-security-profile-model-T42-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-security-profile-model-T42-a01.md
masked 0 match(es) in .orchestration/validation/dot-shell-sp-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-three-role-constellation-T28-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-three-role-constellation-T28-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-three-role-constellation-T28-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-three-role-constellation-T28-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-T33f-a01-audit-rev2.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-T33f-a01-audit-rev2.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-T33f-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-T33f-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-T33f-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-T33f-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-T33f-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-shim-T33g-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-shim-T33g-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-shim-T33g-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-shim-T33g-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-ua-core-build-shim-T33g-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-full-T9-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T33c-a01-audit-rev2.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T33c-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T33c-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T33c-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T33c-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T36-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T36-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T36-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T41-a01-audit-rev2.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T41-a01-audit-rev2.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T41-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T41-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T41-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T41-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T41-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T51-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T55-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T55-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T55-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-ua-graph-refresh-T55-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-refresh-T5-a01.md
masked 0 match(es) in .orchestration/validation/dot-ua-refresh-policy-T52-a01-audit-f700b14.md
masked 0 match(es) in .orchestration/validation/dot-ua-refresh-policy-T52-a01-audit-f700b14.md.last.md
masked 0 match(es) in .orchestration/validation/dot-ua-refresh-policy-T52-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-ua-refresh-policy-T52-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-ua-refresh-policy-T52-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-ua-refresh-policy-T52-a01.md
masked 0 match(es) in .orchestration/validation/dot-ubuntu-fix-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-ubuntu-parity-T2-a01.md
masked 0 match(es) in .orchestration/validation/dot-ubuntu-parity-T3-a01.md
masked 0 match(es) in .orchestration/validation/dot-ubuntu-parity-T4-a01.md
masked 0 match(es) in .orchestration/validation/dot-ubuntu-parity-T5-a01.md
masked 0 match(es) in .orchestration/validation/dot-ubuntu-parity-T6-a01.md
masked 0 match(es) in .orchestration/validation/dot-ubuntu-parity-T7-a01.md
masked 0 match(es) in .orchestration/validation/dot-ubuntu-parity-T8-a01.md
masked 0 match(es) in .orchestration/validation/dot-ubuntu-parity-T9-a01.md
masked 0 match(es) in .orchestration/validation/dot-update-conv-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-update-convergence-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit-1128abb.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit-1128abb.md.last.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit-c636452.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit-c636452.md.last.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-crit-comments.json
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pin-path-codify-T54-a01.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pins-T2-a01.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pins-sync-T37-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pins-sync-T37-a01-audit.md.last.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pins-sync-T37-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-upgrade-pins-sync-T37-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-pins-sync-T37-a01.md
masked 0 match(es) in .orchestration/validation/dot-upgrade-regen-T1-a01.md
masked 0 match(es) in .orchestration/validation/dot-validator-worktrees-T7-a01.md
masked 0 match(es) in .orchestration/validation/dot-version-currency-T29-a01-audit.md
masked 0 match(es) in .orchestration/validation/dot-version-currency-T29-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-version-currency-T29-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-version-currency-T29-a01.md
masked 0 match(es) in .orchestration/validation/dot-worker-advisor-fable-T26-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-worker-advisor-fable-T26-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-worker-advisor-fable-T26-a01.md
masked 0 match(es) in .orchestration/validation/dot-worker-kind-guard-T14-a01.md
masked 0 match(es) in .orchestration/validation/dot-worker-profile-opus55-T24-a01-crit.json
masked 0 match(es) in .orchestration/validation/dot-worker-profile-opus55-T24-a01-receipt.md
masked 0 match(es) in .orchestration/validation/dot-worker-profile-opus55-T24-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-audit-bc001fc.md
masked 0 match(es) in .orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-audit-bc001fc.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-worker-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T62-claude-auto-deny-a01-audit-de8b8b2.md
masked 0 match(es) in .orchestration/validation/dotfiles-T62-claude-auto-deny-a01-audit-de8b8b2.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T62-claude-auto-deny-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T62-claude-auto-deny-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T62-claude-auto-deny-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T62-claude-auto-deny-a01-worker-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T62-claude-auto-deny-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T62-claude-auto-deny-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-04d6e1f3.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-04d6e1f3.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-1f4f409a.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-1f4f409a.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-34e7423f.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-34e7423f.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-7a7c21cd.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-7a7c21cd.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-7e83ed9c.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-7e83ed9c.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-8770ed66.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-8770ed66.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-a0b05905.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-a0b05905.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-c58e4835.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-c58e4835.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-ddb7bf16.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-ddb7bf16.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-e16012eb.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-e16012eb.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-eb67299c.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-audit-eb67299c.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-audit-b9c1aefa.md
masked 0 match(es) in .orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-audit-b9c1aefa.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-audit-d950ac69.md
masked 0 match(es) in .orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-audit-d950ac69.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T64-codex-worker-never-network-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T64-codex-worker-never-network-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-13340185.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-13340185.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-1845139e.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-1845139e.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-3568b7e2.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-3568b7e2.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-4dfceb6e.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-4dfceb6e.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-5a9f35f5.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-5a9f35f5.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-775a527a.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-775a527a.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-8262be37.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-8262be37.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-8433a01b.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-8433a01b.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-92cad32.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-92cad32.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-a62fce9d.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-a62fce9d.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-a9a85ecf.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-a9a85ecf.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-bc636cb7.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-bc636cb7.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-cb3ded43.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-cb3ded43.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-e11659ac.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-e11659ac.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-ea112e2e.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-ea112e2e.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-fd8aa36.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-fd8aa36.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T65-agent-stop-gate-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-8ae3fdc9.md
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-8ae3fdc9.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-a31dcf86.md
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-a31dcf86.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-a93fcb94.md
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-audit-a93fcb94.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T66-permgate-dead-lanes-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T67-audit-task-level-a01-audit-28373e27.md
masked 0 match(es) in .orchestration/validation/dotfiles-T67-audit-task-level-a01-audit-28373e27.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T67-audit-task-level-a01-audit-9476141f.md
masked 0 match(es) in .orchestration/validation/dotfiles-T67-audit-task-level-a01-audit-9476141f.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T67-audit-task-level-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T67-audit-task-level-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T67-audit-task-level-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T67-audit-task-level-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-3ba270d.md
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-3ba270d.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-4fe3427.md
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-4fe3427.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-5168613.md
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-5168613.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-5168613.md.last.md.round1
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-5168613.md.round1
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T68-gate-audit-evidence-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-4656f19.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-4656f19.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-6b060ac.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-6b060ac.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d31dc32.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d31dc32.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d9bbd80.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-audit-d9bbd80.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T69-protocol-docs-unification-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T70-make-update-unattended-a01-audit-229a2ec1.md
masked 0 match(es) in .orchestration/validation/dotfiles-T70-make-update-unattended-a01-audit-229a2ec1.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T70-make-update-unattended-a01-audit-95acd5b6.md
masked 0 match(es) in .orchestration/validation/dotfiles-T70-make-update-unattended-a01-audit-95acd5b6.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T70-make-update-unattended-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T70-make-update-unattended-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T70-make-update-unattended-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T70-make-update-unattended-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-3ecb487.md
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-3ecb487.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-c7b5fb3.md
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-c7b5fb3.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-ef4324d.md
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01-audit-ef4324d.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T71-generator-multi-target-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-audit-d5856e2.md
masked 0 match(es) in .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-audit-d5856e2.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-audit-60688d49.md
masked 0 match(es) in .orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-audit-60688d49.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T73-tool-versions-from-config-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md
masked 0 match(es) in .orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md
masked 0 match(es) in .orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T75-shell-dead-code-a01-audit-339c1496.md
masked 0 match(es) in .orchestration/validation/dotfiles-T75-shell-dead-code-a01-audit-339c1496.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T75-shell-dead-code-a01-audit-ef5742f9.md
masked 0 match(es) in .orchestration/validation/dotfiles-T75-shell-dead-code-a01-audit-ef5742f9.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T75-shell-dead-code-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T75-shell-dead-code-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T75-shell-dead-code-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T75-shell-dead-code-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-26a882a.md
masked 0 match(es) in .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-26a882a.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-f805ee3.md
masked 0 match(es) in .orchestration/validation/dotfiles-T76-ineffective-settings-a01-audit-f805ee3.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T76-ineffective-settings-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T76-ineffective-settings-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T76-ineffective-settings-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T76-ineffective-settings-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T77-harness-dead-code-a01-audit-977bdf1.md
masked 0 match(es) in .orchestration/validation/dotfiles-T77-harness-dead-code-a01-audit-977bdf1.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T77-harness-dead-code-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T77-harness-dead-code-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T77-harness-dead-code-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T77-harness-dead-code-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-audit-43d45ff.md
masked 0 match(es) in .orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-audit-43d45ff.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-worker-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md
masked 0 match(es) in .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T78-dead-docs-adh-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T78-dead-docs-adh-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T79-remove-adh-profile-a01-audit-123bf10.md
masked 0 match(es) in .orchestration/validation/dotfiles-T79-remove-adh-profile-a01-audit-123bf10.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T79-remove-adh-profile-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T79-remove-adh-profile-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T79-remove-adh-profile-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T79-remove-adh-profile-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T80-codex-command-hooks-a01-audit-8a4cf12.md
masked 0 match(es) in .orchestration/validation/dotfiles-T80-codex-command-hooks-a01-audit-8a4cf12.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T80-codex-command-hooks-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T80-codex-command-hooks-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T80-codex-command-hooks-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T80-codex-command-hooks-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-audit-8c8cf69.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-audit-8c8cf69.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-audit-a1c69c4.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-audit-a1c69c4.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T81-compactiondb-vendor-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81-compactiondb-vendor-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-a536af5.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-a536af5.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-b9acaa3.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-b9acaa3.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-worker-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-7ee9108.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-7ee9108.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-94761d1.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-94761d1.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-9ff2ad5.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-9ff2ad5.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-c466231.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-c466231.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T83-docs-diet-a01-audit-914c765.md
masked 0 match(es) in .orchestration/validation/dotfiles-T83-docs-diet-a01-audit-914c765.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T83-docs-diet-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T83-docs-diet-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T83-docs-diet-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T83-docs-diet-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T84-orchestrator-kind-a01-audit-26e748e.md
masked 0 match(es) in .orchestration/validation/dotfiles-T84-orchestrator-kind-a01-audit-26e748e.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T84-orchestrator-kind-a01-audit-55f4d43.md
masked 0 match(es) in .orchestration/validation/dotfiles-T84-orchestrator-kind-a01-audit-55f4d43.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T84-orchestrator-kind-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T84-orchestrator-kind-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T84-orchestrator-kind-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T84-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-audit-20361c5.md
masked 0 match(es) in .orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-audit-20361c5.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01-audit-567c8d1.md
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01-audit-567c8d1.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01-audit-63a9b10.md
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01-audit-63a9b10.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01-worker-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T86-codex-orchestrate-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-0189cfb.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-0189cfb.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-04fd942.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-04fd942.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-19becfc.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-19becfc.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-5bef558.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-5bef558.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-62845ab.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-62845ab.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-e50150df.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-e50150df.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-e68eb6a7.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-e68eb6a7.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-fb4c9a9.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-audit-fb4c9a9.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T88-parallel-execution-rule-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-37cf5e47.md
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-37cf5e47.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-55d7e77c.md
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-55d7e77c.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-958468ba.md
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-audit-958468ba.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-audit-5db3200.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-audit-5db3200.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-worker-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-1af78d7.md
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-1af78d7.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-35d102b7.md
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-35d102b7.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-ffddc8a.md
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-audit-ffddc8a.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T91-secret-scan-sk-boundary-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-153a647.md
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-153a647.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-3371cc8.md
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-3371cc8.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-bbd3d3f.md
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-audit-bbd3d3f.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-254d9eb.md
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-254d9eb.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-aa5b061.md
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-aa5b061.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-dd155f2.md
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-audit-dd155f2.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T94-upgrade-pins-a01-audit-6f5c776.md
masked 0 match(es) in .orchestration/validation/dotfiles-T94-upgrade-pins-a01-audit-6f5c776.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T94-upgrade-pins-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T94-upgrade-pins-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T94-upgrade-pins-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T94-upgrade-pins-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-audit-b9beca2.md
masked 0 match(es) in .orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-audit-b9beca2.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-audit-3a06011.md
masked 0 match(es) in .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-audit-3a06011.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-391d2b4.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-391d2b4.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-5b6b0d9.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-5b6b0d9.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-8ffa554.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-8ffa554.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-efe6735.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-audit-efe6735.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-6ce4e3b.md
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-6ce4e3b.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-aa55684.md
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-aa55684.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-aceb1b1.md
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-audit-aceb1b1.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01.md
masked 0 match(es) in .orchestration/validation/dotfiles-T99-nix-plans-history-a01-audit-43eeb91.md
masked 0 match(es) in .orchestration/validation/dotfiles-T99-nix-plans-history-a01-audit-43eeb91.md.last.md
masked 0 match(es) in .orchestration/validation/dotfiles-T99-nix-plans-history-a01-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T99-nix-plans-history-a01-pr-feedback.json
masked 0 match(es) in .orchestration/validation/dotfiles-T99-nix-plans-history-a01-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-crit.json
masked 0 match(es) in .orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/validation/dotfiles-T99-nix-plans-history-a01.md
masked 0 match(es) in .orchestration/validation/fix-chezmoi-pycache-modify-exec-crit-comments.json
masked 0 match(es) in .orchestration/validation/fix-chezmoi-pycache-modify-exec-review-receipt.md
masked 0 match(es) in .orchestration/validation/fix-chezmoi-pycache-modify-exec.txt
masked 0 match(es) in .orchestration/validation/orchestration-boundary-2026-10-03-pr-feedback.json
masked 0 match(es) in .orchestration/validation/plan-001.md
masked 0 match(es) in .orchestration/validation/plan-002-crit-comments.json
masked 0 match(es) in .orchestration/validation/plan-002-crit-structure.json
masked 0 match(es) in .orchestration/validation/plan-002.md
masked 0 match(es) in .orchestration/validation/plan-003-pr-final.md
masked 0 match(es) in .orchestration/validation/plan-003.md
masked 0 match(es) in .orchestration/validation/plan-004.md
masked 0 match(es) in .orchestration/validation/remote-diff-01.md
exit=0
```

## Bot wait on the diff head 70f060e7 (SKILL step 15; full log)

Each poll counts reviews, top-level inline comments, and quota-notice issue comments posted after the wait started.

```
start 2026-10-05T09:29:54Z head=70f060e74c64e3da3f7dfa251f98d9e43a8b5105
poll 1 2026-10-05T09:29:55Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 2 2026-10-05T09:30:26Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 3 2026-10-05T09:30:57Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 4 2026-10-05T09:31:29Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 5 2026-10-05T09:32:00Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 6 2026-10-05T09:32:31Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 7 2026-10-05T09:33:02Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 8 2026-10-05T09:33:34Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 9 2026-10-05T09:34:05Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 10 2026-10-05T09:34:37Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 11 2026-10-05T09:35:08Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 12 2026-10-05T09:35:39Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 13 2026-10-05T09:36:11Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 14 2026-10-05T09:36:42Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 15 2026-10-05T09:37:13Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 16 2026-10-05T09:37:44Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 17 2026-10-05T09:38:16Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 18 2026-10-05T09:38:47Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 19 2026-10-05T09:39:18Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 20 2026-10-05T09:39:49Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 21 2026-10-05T09:40:21Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 22 2026-10-05T09:40:52Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 23 2026-10-05T09:41:23Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 24 2026-10-05T09:41:54Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 25 2026-10-05T09:42:26Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 26 2026-10-05T09:42:57Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 27 2026-10-05T09:43:28Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 28 2026-10-05T09:43:59Z bot_reviews=0 bot_comments=0 quota_notices=0
poll 29 2026-10-05T09:44:31Z bot_reviews=0 bot_comments=0 quota_notices=0
end 2026-10-05T09:45:01Z
```

After the wait: the Bot reviews (bodies included), the Bot issue comments, and the top-level Bot inline threads:

```
[]
```

```
[
{
"body": "Codex usage limits have been reached for code reviews. Please check with the admins of this repo to increase the limits by adding credits.\nRepo admins can enable using credits for code reviews in their [settings](https://chatgpt.com/codex/cloud/settings/code-review).",
"created_at": "2026-10-05T09:13:55Z",
"id": 5991528439
},
{
"body": "<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This is an auto-generated comment: skip review by coderabbit.ai -->\n\n> [!IMPORTANT]\n> ## Review skipped\n> \n> Auto reviews are disabled on this repository. Please check the settings in the CodeRabbit UI or the `.coderabbit.yaml` file in this repository. To trigger a single review, invoke the `@coderabbitai review` command.\n> \n> <details>\n> <summary>⚙️ Run configuration</summary>\n> \n> - **Configuration used**: Repository: mryfmo/dotfiles/.coderabbit.yaml\n> - **Review profile**: CHILL\n> - **Plan**: Advanced\n> - **Run ID**: `782f8b14-906f-467e-b489-1bec1f272cc7`\n> \n> </details>\n> \n> You can disable this status message by setting the `reviews.review_status` to `false` in the CodeRabbit configuration file.\n> \n> Use the checkbox below for a quick retry:\n> - [ ] <!-- {\"checkboxId\":\"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe\"} --> 🔍 Trigger review\n\n<!-- end of auto-generated comment: skip review by coderabbit.ai -->\n\n<!-- autopilot:start -->\n- [ ] <!-- {\"checkboxId\":\"2708ad07-9f24-4260-9c11-7dc76a49f2e3\"} --> <strong title=\"Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\">Autopilot</strong> · Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts\n<!-- autopilot:end -->\n<!-- tips_start -->\n\n---\n\nThanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=mryfmo/dotfiles&utm_content=280)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.\n\n<details>\n<summary>❤️ Share</summary>\n\n- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)\n- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)\n- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)\n- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)\n\n</details>\n\n\n<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>\n\n<!-- tips_end -->",
"created_at": "2026-10-05T09:14:00Z",
"id": 5991529584
}
]
```

```
[]
```

## CompactionDB (main checkout; command as executed, plus readback)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T98b (orchestrator 2026-10-05): `~` and `~` are machine-independent anywhere-forms of the home-path masker and scan, and Bot review-body findings are swept and dispositioned like inline threads (Worker step 15, Orchestrator step 10.4).'
5328b485-c4ed-4859-8242-2498b0156b0a
exit=0
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search T98b --session 79f0f3c0-a708-4c6f-affe-0d87fcc6ba5a
5328b485-c4ed-4859-8242-2498b0156b0a [project/decision] dotfiles-T98b (orchestrator 2026-10-05): `~` and `~` are machine-independent anywhere-forms of the home-path masker and scan, and Bot review-body findings are swept and dispositioned like inline threads (Worker step 15, Orchestrator step 10.4).
exit=0
```


## Masking these artifacts (last step, from the main checkout`s .orchestration directory)

```
$ uv run --no-project --with pyyaml <worktree>/scripts/validate-agent-assets.py --mask-secrets reports/dotfiles-T98b-runner-home-and-review-body-a01.md validation/dotfiles-T98b-runner-home-and-review-body-a01.md sandboxes/dotfiles-T98b-runner-home-and-review-body-a01.md learning/dotfiles-T98b-runner-home-and-review-body-a01.md autoskill/runs/dotfiles-T98b-runner-home-and-review-body-a01.md
masked 2 match(es) in reports/dotfiles-T98b-runner-home-and-review-body-a01.md
masked 14 match(es) in validation/dotfiles-T98b-runner-home-and-review-body-a01.md
masked 0 match(es) in sandboxes/dotfiles-T98b-runner-home-and-review-body-a01.md
masked 0 match(es) in learning/dotfiles-T98b-runner-home-and-review-body-a01.md
masked 0 match(es) in autoskill/runs/dotfiles-T98b-runner-home-and-review-body-a01.md
mask exit=0
```
