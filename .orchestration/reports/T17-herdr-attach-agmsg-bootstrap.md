# T17 worker report

## Status

Ready for review on `feat/herdr-attach-order-repair`.

## Changes

- Added best-effort `bootstrap_agmsg` after Codex start/reuse in attach,
  existing-workspace, and new-workspace success paths.
- Skip silently when agmsg delivery is not installed.
- Use a pure jq check of `<repo>/.codex/hooks.json`, traversing the real
  `.hooks.Stop[].hooks[]` schema; an existing agmsg `check-inbox.sh` Stop hook
  skips `delivery.sh` completely.
- When absent, run `delivery.sh set turn codex <repo>` once with nonfatal
  semantics and append its output to the existing Herdr agents log.
- Verify repo-scoped Codex identities. Missing identity prints a one-line
  warning with the exact `join.sh` form; multiple identities print a one-line
  ambiguity warning. No auto-join or session claim occurs.
- Added one Claude orchestration rule bullet requiring fresh-session and
  persisted-session live E2E before accepting desktop behavior changes.

## Known first-time effect

The first missing-hook call to `delivery.sh set turn` can stop same-repository
watchers once. The steady-state hook-present path never calls delivery and has
zero watcher risk, per the orchestrator amendment.

## Scope

No live agmsg/delivery mutation, live Herdr mutation, chezmoi apply, dependency
change, commit, push, or LLM call was performed by this worker.

## Acceptance revision 2

The hook-present test now uses the producer's real matcher-plus-nested-hooks
shape. The jq query was corrected to inspect each nested command, so repeated
attach skips delivery exactly as required.
