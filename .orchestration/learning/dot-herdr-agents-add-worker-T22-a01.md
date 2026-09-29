# T22 learning triage

## Revision 4

1. **A seat fix must cover every path that starts the agent**, not only the paths that create panes. The heal path's reused empty pane still started the worker in the main checkout. Enumerate every `start_worker_agent` call and check which cwd its pane has.
2. **A host-global manifest value applied per repository needs an applicability gate** that runs before any side effect: main checkout, existing worktree or registration. Otherwise every repository the hook runs in gets side effects.
3. **Test fakes must mirror upstream exit codes.** A fake `identities.sh` that exited 1 on "no rows" hid, and then triggered, a silent `pipefail` + `set -e` exit. Guard lookups with `|| var=""`.
4. **Upstream despawn semantics differ by type:** a codex seat never holds the actas lock, so a graceful despawn ends `needs-force`. Read the teardown contract per type before designing a flag.
5. **An independent adversarial review found a P1 again** that my own tests missed, as in T19. Keep the review step before RESULT.

## Promotion

None. These are candidates only; promotion is the orchestrator's call.

## Revision 4b

6. **Never force a teardown unconditionally.** Upstream `despawn.sh --force` needs the placement record, which a failed spawn never writes. Follow the tool's own escalation signal (`status=needs-force`) instead of assuming a type-based rule.
