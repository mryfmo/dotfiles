# T20 validation evidence

## Test-first evidence

Before implementation, the five new bootstrap-only tests all failed with exit
2 because `--bootstrap-agmsg` was not recognized:

```text
Ran 5 tests in 0.627s
FAILED (failures=5)
```

The implementation then made the focused contract green, including real
nested Claude schema detection, one call per missing side, missing/multiple
identity warnings, and zero Herdr mutations.

## Unit and static validation

```text
$ uv run python -m unittest tests.unit.test_herdr_agents -v
Ran 58 tests in 6.019s
OK

$ make unit-test
Ran 175 tests in 16.011s
OK

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

$ bash -n home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ shellcheck home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ git diff --check
# exit 0, no output
```

Local bats tests were not run, per repository policy.

## Scratch repository E2E

The real installed agmsg scripts were exposed through an isolated scratch HOME
and run only against `/private/tmp/t20-agmsg-setup-automation`.

First bootstrap created both files using the producer's schemas:

```text
.codex/hooks.json:
  .hooks.Stop[].hooks[].command contains agmsg/scripts/check-inbox.sh

.claude/settings.local.json:
  .hooks.SessionStart[].hooks[].command contains agmsg/scripts/session-start.sh
  .hooks.SessionEnd[].hooks[].command contains agmsg/scripts/session-end.sh
  .hooks.Stop[].hooks[].command contains agmsg/scripts/check-inbox.sh
```

Real delivery status reported:

```text
codex:       mode: turn
claude-code: mode: both
```

A second bootstrap was run under `bash -x`; the trace inspected both hook files
and contained no delivery command. `make agmsg-bootstrap` was then rerun twice.
The delivery log remained 16 lines and both hook hashes remained unchanged:

```text
ddddd6883bb2deb2b1a21db6583493e9387ab8ba1f973b87cd2230b83efbd8b5  .codex/hooks.json
e1b335f59d6dd3671e65dccba1f334c66b535fcb03a4b4bffe5d98a8184df2e3  .claude/settings.local.json
```

An isolated scratch `watch.sh` PTY session was running before the repeated
bootstrap and Make calls. Polling the same exec session afterward returned
`Process running`, proving it survived both idempotent paths; it was then
stopped with Ctrl-C.

## Make integration and missing assets

`make -n update` showed `update-agent-assets`, the existing Herdr config reload,
then recursive `make agmsg-bootstrap`. `make -n upgrade` showed
`upgrade-tools` then recursive `make agmsg-bootstrap`.

Missing assets degrade explicitly:

```text
agmsg delivery script not found; skipping bootstrap: <scratch-home>/.../delivery.sh
Herdr agents source helper not found; skipping agmsg bootstrap.
```

## Pull request and CI

- PR: https://github.com/mryfmo/dotfiles/pull/79
- Commit: `907ed02`
- Final GitHub Actions status: all applicable checks passed.
- CodeRabbit status: passed; no actionable review findings.
- Nix status: skipped by the workflow's change filter.

## Deployment acceptance

PR #79 was squash-merged and local `main` was fast-forwarded to:

```text
54f1fff095c9296e58a86be7a2e2415c4c54f37a
```

A real `make update` was then run from
`/Users/mryfmo/Workspace/dotfiles`. It exited 0. The complete 338-line output
is captured at
`/private/tmp/T20-agmsg-setup-automation-make-update.log` with SHA-256:

```text
18cadc67e087cdaacb16d111d12a0846dd1d5ada4b395b0a04680c5b04afda29
```

The output ends with the new explicit step:

```text
/Library/Developer/CommandLineTools/usr/bin/make agmsg-bootstrap
Multiple agmsg Claude Code identities are registered for /Users/mryfmo/Workspace/dotfiles; worker identity is ambiguous.
```

Steady-state evidence before and after the real update was identical:

```text
.codex/hooks.json
3b07ad1b10405388ae0abfee70f3ceb82a14355a4c339b922055bef4a00c957d

.claude/settings.local.json
b1ffde6450b807f75a5e87407541389ee1ce4b28d336700af263e7a73486fa92

~/.config/herdr/herdr-agents.log
47 lines

delivery status
codex: turn
claude-code: both
```

The same live Claude Code watcher survived the update:

```text
wrapper PID: 99013
watch.sh PID: 99017
session: 5643c3ca-540b-4cad-8bf4-cf97f9e8928b
project: /Users/mryfmo/Workspace/dotfiles
type: claude-code
```

The real `make upgrade` target was not run; its prior `make -n` evidence
remains the accepted proof. The `/private/tmp/dotfiles-t20` worktree and local
`feat/agmsg-setup-automation` branch were removed.
