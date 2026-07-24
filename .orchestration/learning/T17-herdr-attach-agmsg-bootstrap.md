# T17 learning triage

## Candidate reusable rule

An unconditional idempotent-looking configuration command may still have
process side effects. Before bootstrapping delivery, inspect the repo hook file
directly and skip the command when the required hook is already installed.
This makes steady-state application startup side-effect free.

Configuration-schema tests must mirror the producing tool's actual nesting.
Checking a command field on the matcher object gave false confidence because
the real Codex hook stores commands in `.hooks.Stop[].hooks[]`.

## Apply to

- Bootstrap plans that call delivery/configuration commands during application
  start.
- Tests should cover absent, present, unavailable, and failing bootstrap paths.
- Hook fixtures should use a captured or producer-derived schema rather than a
  simplified shape.
- Live desktop behavior acceptance must cover both fresh and persisted
  sessions.

## Promotion

No direct promotion; promotion decisions remain with the orchestrator.
