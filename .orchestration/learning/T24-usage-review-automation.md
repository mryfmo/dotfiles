# T24 learning triage

## Candidates

- launchd does not inherit an interactive shell PATH; scheduled commands that
  rely on mise shims need an explicit `EnvironmentVariables.PATH`.
- launchd `StartCalendarInterval.Weekday` uses `1` for Monday; `0` and `7`
  represent Sunday.
- A missing-command test must isolate PATH, not only remove its local stub,
  because CI runners may provide that command in a system directory.
- Idempotency that must survive concurrent scheduling needs atomic no-replace
  publication, not only an existence check before `mv`.

## Evidence

- PR review identified the launchd PATH/weekday and concurrency issues.
- The first CI run demonstrated the system-gh PATH leak on macOS and Ubuntu.
- The final implementation passed 191 local tests, shell/plist validation, and
  all GitHub Actions jobs.

## Decision

Reusable and validated. Promoted to
`.agents/worklog/codex/learn/20260723_190547_learn.md` and indexed.

## Plan updates

The T24 plan assumptions and tests now record the explicit launchd PATH,
Monday weekday value, keyed ccusage breakdown support, atomic snapshot
publication, and isolated missing-command fixture.

## After acceptance

The validated implementation was squash-merged and main was synchronized with
a clean ff-only update. The reusable learn entry remains in the worklog index.
