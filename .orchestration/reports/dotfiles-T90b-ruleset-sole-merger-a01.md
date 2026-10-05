---
type: report
id: 20261005_032100
owner: codex-security-dot-a007
status: done
created_at: 2026-10-05T03:21:00+09:00
updated_at: 2026-10-04T18:55:09.457972+00:00
---
# T90b plan / TODO

Task SHA256 initial: 092892d896a0676d2fb5ef4b984ed16de76eeaca0127a83ef0c1253b0572d764; PONG decision revision verified: cd24dd1c15d8fbe44c38d4e04351debdf6fa79f58707c6d5f17d82f8cee3a3b3; PONG decision 2 revision verified: d76748b0d53276a02084a781383a1c92f2e32f3a60a6bdd281b7ac34eef4f4db; PONG decision 3 verified: 2d90374b237b468c601b30f37271ebe03bf4e2ea840ce484f2599d6435c5d1b1.

## Current result

PR https://github.com/mryfmo/dotfiles/pull/265, head5db320019d4c63f31eed9bfc1cea88ddade0a7cb from main4c38dea07ff2cf448909c0773f6e8332930be090. Local783 full /76 focused tests pass, independent final review correct after mirrored-rule P2 correction. Final-head CI all passes, mergeable=true and mergeable_state=clean on main4c38dea0. Final-head Bot wait 2026-10-04T18:39:32Z–18:54:33Z ended at the 15-minute bound with bot: none. No review threads exist (pagination complete). Final local review gate passed. Ready for orchestrator acceptance. No live activation.

## Goal
Make GitHub main updates exclusive to the orchestrator through pull-request-only bypass; preserve boundary PRs and existing checks.

## Scope
Five allowed source/test/document paths and seven task artifacts. No launcher/credential/account/ruleset application/merge. Own worktree, branch feat/ruleset-sole-merger from merged T90 main 4c38dea0. Prior T90 artifacts retained unchanged.

## Assumptions
.agents is read-only, so plan/TODO fallback is this uncommitted report. Stale UA graph remains intentionally untouched. Orchestrator records the CompactionDB decision/output at acceptance.

## Design
Activate role gate when worker hosts.yml exists and effective main rules include update or required approval. Verify sole User bypass actor against authenticated user ID; only an orchestration-only PR authored by that login is exempt from approval. Worker PR still needs current-head approval. GitHub docs support User actor IDs and pull_request bypass; bypass covers all rules in the containing ruleset.

## Tests
Write activation/authorship/bypass regression tests first, then focused/full Python unit suites. Assets, Ruff format, Prettier, independent security review, review gate, GitHub CI and bounded Bot wait. No local bats.

## Open Questions
Resolved by authorized split: no-bypass integrity ruleset retains seven strict checks, thread resolution, deletion and non-fast-forward protections; merge-control ruleset contains update and approval with sole User PR-only bypass. Local disposition policy unchanged; server-side integrity remains enforcing. Live operator scratch tests are not performed here. Second VERIFY finding: gh merge preflight and auto completion do not engage the required bypass path. PONG decision 2 authorizes synchronous merge PUT with exact head SHA and commit title for both boundary and acceptance.

## TODO
None for worker implementation; acceptance and operator activation remain as listed below.

## Done
Task verified; dedicated branch created. Read-only GitHub repository/rules queries and primary docs examined.

cost: n/a

## Implementation / verification

Read-only GitHub GET confirmed repository owner type User, current ruleset24397953 has required approval0 and no update restriction, and mryfmo numeric userID11512262. The current default token does not expose bypass_actors on GET: activated gate deliberately fails closed on missing metadata rather than treating missing actors as permission. Operator must authenticate the configured orchestrator.

Only effective rulesets containing update or positive approval requirements need the sole User PR-bypass check. The no-bypass integrity layer has approval0, so it remains outside that actor check while GitHub enforces its CI/thread constraints. Every restricting ruleset must agree on sole actor/current authenticated ID. A zero-approval-only transition remains inactive. A self-authored exception checks all nonempty committed paths using NUL separation and --no-renames; review-sizing ignores cannot hide tracked non-orchestration changes.

Independent initial and full-diff reviews found no functional gate defect and supported the split; final docs re-review includes the synchronous-merge correction. Added combined rulesets, mismatched second restriction, missing metadata/API failure, cross-boundary rename and empty-diff coverage after review.

CompactionDB main checkout remains outside this seat's writable roots. Orchestrator records the final corrected decision and memory-add output in acceptance. No memory command executed here.

## VERIFY sources

- https://docs.github.com/en/rest/repos/rules?apiVersion=2026-03-10#update-a-repository-ruleset : User actor numeric ID, pull_request bypass mode, bypass is scoped to the containing ruleset; update restricts ref updates to bypass actors.
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#restrict-updates : updates restricted to bypass users. Blocking merges follows because merging updates the protected ref; this inference remains subject to operator live checks.
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository#granting-bypass-permissions-for-your-branch-or-tag-ruleset : PR-only bypass disallows direct pushes and can bypass protections in its ruleset.
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets#about-rule-layering : applicable rulesets all apply and stricter restrictions combine. The integrity ruleset has no bypass; role bypass cannot remove its protections.
- https://docs.github.com/en/rest/pulls/pulls?apiVersion=2026-03-10#merge-a-pull-request : synchronous merge API HTTP200 success,405 unavailable,409 SHA mismatch.
- https://github.com/cli/cli/blob/v2.101.0/pkg/cmd/pr/merge/merge.go : installed-version source rejects BLOCKED before ordinary merge and routes --auto to enable-auto instead of synchronous merge.
- https://github.com/cli/cli/issues/13388 and https://github.com/github/docs/issues/45265 : upstream direct reproductions of bypass ignored by CLI preflight/auto completion, but respected by synchronous REST merge. Both open at verification; actual local ruleset rollout remains unperformed.

## Remaining operator work
Provision distinct role accounts, run doctor, restart/verify worker logins, update no-bypass integrity first then create/update merge control, and perform README scratch checks (self-approval denied; worker merge denied before/after approval; orchestrator/boundary synchronous merges succeed with SHA guard; direct pushes and integrity failures denied). No credential/account/ruleset mutation, merge or launcher edit performed by this task.

Final local validation: 783 unit tests passed in 200.299s; focused role/review guard suite 76 passed. Prettier, Ruff format and asset validation passed; asset warnings only describe pending orchestration artifacts/live worker seats. Two legacy SKILL boundary --auto references now explicitly apply before activation and point to step10.5 afterward (PONG decision3).

PONG decision4 verified: 603610563d25d83ea90389d5ddfe21d4ffcc1305131f91feedc94f483d42f8d4. Independent final review found a P2 stale merge-command reference in the mirrored rule line9; authorized replacement points to SKILL10.5. All other remaining gh merge references are now preactivation-qualified or descriptive warnings.

## Final handoff

All seven task artifacts are ready for transfer. Task revision at completion: 603610563d25d83ea90389d5ddfe21d4ffcc1305131f91feedc94f483d42f8d4. Worker performed no GitHub merge or ruleset mutation. Final audit, feedback sweep, acceptance/merge and CompactionDB recording belong to orchestrator; live activation belongs to operator.
