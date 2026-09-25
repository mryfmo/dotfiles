# T87 Acceptance — boundary bookkeeping after #147

status: accepted
task: .orchestration/tasks/T87-boundary-bookkeeping-147.md
result: AGMSG-RESULT 2026-08-29T06:30:52Z (ready_for_review)
prs: #150 (chore/ua + .orchestration tail), #148 (agmsg template), #149 (mise pair)
cost: n/a

## Adversarial review (orchestrator-side)

- Class purity independently verified via `gh pr view --json files` on all
  three PRs: #148 = template only; #149 = the mise config/lock pair only
  (three same-class commits that squash to one); #150 = `.ua/` (3 files) +
  the complete T86/T87 `.orchestration` audit tail. No cross-class leakage.
- CI independently confirmed: 12 passing checks on each PR, none failing or
  pending (`nix` skipped by workflow condition).
- Refutation attempt on PR C's "retain CI-pinned versions" decision: the
  worker reverted the `make upgrade` bumps for ccusage and herdr, leaving the
  repo pin at herdr 0.8.0 while the live machine runs 0.8.2 and the T86
  launcher targets the current agent API. Resolved against upstream release
  notes: the `agent start --kind/--pane` contract landed in herdr v0.7.5, so
  the 0.8.0 pin remains launcher-compatible; retaining it preserves main's
  status quo and introduces no regression. Residual: `pane split --env`
  availability on 0.8.0 is not covered by changelogs — low risk (pre-0.7.5
  scripts already passed `--env`), revisit when a separate upgrade-class task
  moves the pins.
- UA update audit: partial refresh of exactly the two paths changed by #147;
  3 nodes replaced in place with IDs preserved; 0 dangling edges; unchanged
  regions JSON-identical to baseline; known pitfalls (nested FingerprintStore,
  extensionless shell fingerprints) explicitly handled per the learning file.
- Boundary invariant: canonical checkout has zero untracked `.orchestration`
  tail; this acceptance record itself rides in PR #150 so the invariant holds
  post-merge as well.
- CompactionDB: consolidated decision `241a29fe-e690-4812-b7cf-9bcbdeb3fbdc`
  present; T86's two decisions verified earlier.
- effects: none.

## Integration notes

- The local dirty copies of the template and mise pair (pre-revert upgrade
  bumps) are superseded by the merged, CI-validated versions; snapshots kept
  in the session scratchpad before discard. A future upgrade-class task may
  re-bump ccusage/herdr together with their CI contracts.
- next_action: merge #148, #149, #150; discard superseded dirty copies; pull
  main; verify zero tail.
