# T83b acceptance

- task: T83b (UA freshness semantics + edge restoration, PR #138 P2 x2)
- decision: accepted
- date: 2026-08-17
- reviewer: claude-deep-dot (orchestrator)

## Adversarial review

- Freshness fix verified in both policy diffs: exactly one replaced
  sentence each, semantics = current when hash matches HEAD or the
  intervening diff lists only `.ua/`/`.orchestration/` paths; no rule
  regrowth (files stay 8 and 68 lines).
- Edge audit: complete removed-edge set (31) classified, no sampling;
  23 restored (including both named dependencies and all ten
  template documentation edges), 8 correctly left removed because the
  dieted core rule genuinely no longer documents those scripts (their
  coverage moved to the skill). 934 -> 957 edges, node count stable,
  validator success=true, no dangling endpoints.
- Gates re-run orchestrator-side: 336 unit tests OK,
  validate-agent-assets ok.
- Integration ordering issue identified by the worker and adopted:
  policy-source commit first, then a mechanical meta.gitCommitHash
  re-pin to that commit (the graph analyzed the tree including the
  policy edits), then the graph/evidence-only commit — otherwise the
  new freshness rule itself would mark the graph stale.

## Effects

effects=none.

cost: n/a (worker-reported)
