# T20 learning triage

## Candidate reusable rule

Expose stateful bootstrap logic through a side-effect-narrow CLI entrypoint and
reuse that entrypoint from lifecycle automation. This keeps startup and Make
behavior on one implementation while allowing tests and operators to prove
that no unrelated UI or agent mutation occurs.

Idempotency for configuration tools must be established before invoking the
tool, not inferred from the tool's eventual file output. A no-op-looking
configuration rewrite may still stop runtime processes.

## Apply to

- Bootstrap helpers called from application startup and repository lifecycle
  targets.
- Tests for hook-based configuration should mirror the producer's nested
  schema and assert invocation count, not only final file content.
- E2E validation of process-safe idempotency should hold a real isolated
  process open across both direct and automated reruns.

## Promotion

No direct promotion; the orchestrator owns any shared-rule promotion.
