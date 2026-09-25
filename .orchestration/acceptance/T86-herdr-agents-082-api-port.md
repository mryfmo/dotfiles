# T86 Acceptance — herdr-agents 0.8.2 API port

status: accepted
task: .orchestration/tasks/T86-herdr-agents-082-api-port.md
result: AGMSG-RESULT 2026-08-29T05:06:44Z (ready_for_review)
pr: #147 (fix/herdr-agents-herdr-082-api)
cost: n/a

## Adversarial review (orchestrator-side)

- Full PR diff read end-to-end (791 lines, 2 files — exactly the allowed
  source files; `gh pr view --json files` confirms no scope leak; unrelated
  dirty paths `home/dot_mise/*` and the agmsg template drift were left
  unstaged as required).
- Refutation attempts on the port: profile resolution order
  (env > `MODEL_PROFILE_INTERACTIVE` > standard) verified against the
  `resolve_codex_profile` implementation and its two regression tests;
  the readiness guard is bounded (50×0.2s process-info poll + 10s
  wait-output) with a single retry limited to newly created panes; the
  `agent_not_ready` path waits for the already-registered agent instead of
  duplicating it; derived names are lowercased and validated against the
  0.8.2 pattern with a rejection test.
- Independently re-derived validation on the branch: `bash -n` pass,
  `shellcheck` pass, `uv run python -m unittest tests.unit.test_herdr_agents`
  pass (65 tests). CI on PR #147 independently confirmed green
  (`gh pr checks 147`; nix skipped by workflow condition).
- Live E2E evidence reviewed: fresh workspace `w1R` (two panes, lowercase
  agent names), rerun idempotency, `--attach` idempotency, express-profile
  test subjects sourced from the generated manifest, protected `w1F`
  untouched, full teardown recorded. The compaudit/FPATH finding and the
  combined process-info + prompt guard are documented with evidence.
- Crit evidence: 1 resolved review-scope approval record
  (`.agents/worklog/codex/review/20260829_135518_t86_crit.json`); receipt
  carries `review_outcome: approved`.
- CompactionDB: both mandated decision records exist
  (`1d11001e-…`, `ada64692-…`) — consolidation for T86 satisfied.
- Effects: none outside the working tree (E2E artifacts torn down; scratch
  agmsg identity checks were empty). No `effects=` field needed.

## Notes

- E2E used a Claude permission-bypass flag solely inside the disposable
  scratch workspace to skip the first-run trust prompt; acceptable for a
  throwaway test subject, not a precedent for resident agents.
- next_action: merge PR #147, apply the launcher via chezmoi, then boundary
  bookkeeping (UA incremental graph update + .orchestration sync PR, agmsg
  template drift chore, mise config/lock chore as its own commit).
