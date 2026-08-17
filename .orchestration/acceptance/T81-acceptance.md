# T81 acceptance

- task: T81 (worker cost reporting in RESULT report, PLAN-pi-pivot Phase 6)
- decision: accepted
- date: 2026-08-17
- reviewer: claude-deep-dot (orchestrator)

## Adversarial review

- Delta verified as exactly one Worker Playbook item (12): report-artifact
  `cost:` line, runtime-observed figures or `cost: n/a`, cross-referenced
  to the T76 acceptance cost line. No wire-contract field added (Message
  Contract hash unchanged), no rule-file growth, no duplication of the
  existing acceptance-side clause.
- Gates re-run orchestrator-side: 336 unit tests OK, validate-agent-assets
  ok. Consolidated decision UUID 02b024a9 confirmed in main DB.

## Effects

effects=none. Skill copies redeployed orchestrator-side.

cost: n/a (worker-reported)
