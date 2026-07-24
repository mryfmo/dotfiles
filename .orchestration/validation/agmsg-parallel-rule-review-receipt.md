# Review receipt: agmsg-orchestration rule revision (parallel workers)

review_surface: crit-data
reviewer: claude-code
review_source: .orchestration/validation/agmsg-parallel-rule-crit-comments.json
review_outcome: addressed

## Scope

`home/dot_config/claude/rules/agmsg-orchestration.md` — enable same-repo parallel
workers (at most one resident worker per git worktree), profile-based identities
(`<runtime>-<profile>-<project-suffix>[-aNNN]`, model IDs banned from identities),
and lock acceptance/review responsibilities to the orchestrator side.

## Process

Two-round adversarial review by an independent subagent (refutation stance),
verified against the agmsg implementation (check-inbox.sh, whoami.sh,
identities.sh, watch.sh, delivery.sh, herdr-agents). Round 1: 8 findings
(4 blockers). All addressed; the parallel-RESULT-detection blocker was resolved
by adopting a shared-default-store regime for same-repo parallel workers, which
the implementation supports via identity-addressed delivery and exact-path
whoami resolution. Round 2 verdict: sound. Optional hardening (launch-env
verification, byte-identical path wording) applied.
