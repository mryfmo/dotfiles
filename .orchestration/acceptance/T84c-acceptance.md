# T84c acceptance

- task: T84c (bats old modify\_ path sweep, PR #140 P1 + 3 CI fails)
- decision: accepted
- date: 2026-08-18
- reviewer: claude-deep-dot (orchestrator)

## Adversarial review

- Independent repo-wide residue scan re-run orchestrator-side: zero
  non-private `modify_<profile>` references in tests/, scripts/, docs/;
  the single active hit (lifecycle.bats:384) is the one fixed line.
  Historical `.orchestration/` evidence and `.ua/` snapshots preserved
  by design.
- bash -n on the bats body; unit suite and validate-agent-assets green.
- Root context recorded: bats runs only in CI (repo policy), so rename
  sweeps must always cover CI-only suites; T84's allowed_files omission
  was the task-spec gap.

## Effects

effects=none.

cost: n/a (worker-reported)
