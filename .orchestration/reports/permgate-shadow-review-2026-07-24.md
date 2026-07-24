# permgate shadow accuracy review and llm_enabled decision (2026-07-24)

Orchestrator judgment record (orchestrator-fable5), per the T25 acceptance
gate: a provider may be enabled only after reviewed shadow outcomes AND a
five-run `permgate bench` with 5/5 successful classifications, p50 ≤ 3000 ms,
p95 ≤ 7000 ms.

## Evidence reviewed

- Shadow decision data: **none exists**. permgate is merged but not yet
  deployed (`~/.local/bin/common/permgate` absent, no PermissionRequest hook
  in live Claude/Codex settings, no `~/.local/state/permgate/decisions.jsonl`).
  There are zero shadow outcomes to grade for accuracy.
- Bench (T25 validation, corrected live five-run, existing agent auth):
  - Claude: 2/5 successful, p50 6071 ms, p95 7032 ms — fails successes, p50,
    and p95.
  - Codex: 3/5 successful, p50 4911 ms, p95 6859 ms — fails successes and p50.

## Decision

**Keep `llm_enabled: false` for BOTH providers.** No policy change required
(the merged policy already ships shadow). Enablement today would violate the
enforced gate on every axis; the deterministic layer plus native prompts
remain authoritative.

## Revisit criteria

Re-evaluate per provider (independently) only when ALL hold:

1. permgate deployed live (T28) and ≥ 7 days of shadow data in
   `decisions.jsonl`.
2. Shadow accuracy review over that window: every `shadow_decision: allow`
   line re-judged; zero would-be false allows (any false allow → tighten
   policy first, restart the window).
3. Fresh `permgate bench`: 5/5 successes, p50 ≤ 3000 ms, p95 ≤ 7000 ms for
   that provider.

Until then the operational cost is zero: shadow classification only runs for
already-safe normalized actions and never changes the returned decision.
