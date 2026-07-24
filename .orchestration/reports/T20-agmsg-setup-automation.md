# T20 worker report

## Status

Ready for review on `feat/agmsg-setup-automation` at
https://github.com/mryfmo/dotfiles/pull/79 (`907ed02`).

## Changes

- Extended `bootstrap_agmsg` with a real-schema Claude Code gate at
  `.hooks.SessionStart[].hooks[].command`.
- Missing Claude Code hooks invoke exactly
  `delivery.sh set both claude-code <repo>` with nonfatal logging and a
  first-time watcher/next-session notice.
- Codex and Claude Code identities are checked independently. Missing
  identities print exact `join.sh` instructions, and multiple registrations
  print ambiguity warnings. Bootstrap never joins automatically.
- Added `herdr-agents --bootstrap-agmsg [DIR]`, which requires only `jq` and
  performs no Herdr workspace, pane, layout, or agent operations.
- Added `make agmsg-bootstrap` and placed it after the existing `update` and
  `upgrade` steps. Missing source or installed agmsg scripts produce explicit
  skip messages.
- Preserved the canonical `$HOME` guard and the existing Codex trust note.

## Idempotency

- The Codex and Claude Code hook files are inspected before any delivery
  command.
- First setup calls delivery once for each missing side.
- When both hooks already exist, startup and Make bootstrap paths perform zero
  delivery calls.

## Scope

No production repository delivery mode was changed, no live Herdr workspace
was touched, no local bats tests were run, and no dependency, CI, permission,
or agmsg skill implementation was changed.

## CI

All GitHub Actions checks passed after the final force-with-lease update:
agent validation, unit tests on macOS and Ubuntu client/server, and public and
private bootstrap matrices. The Nix job was intentionally skipped by the
workflow's change filter.
