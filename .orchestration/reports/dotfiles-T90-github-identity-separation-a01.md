---
type: report
id: 20261005_014500
owner: codex-security-dot-a007
status: done
created_at: 2026-10-05T01:45:00+09:00
updated_at: 2026-10-04T18:15:49.318944+00:00
---
# T90 result and completed worklog

Task SHA256: initial 72ad7704610dbcd5402307bc05c9d17fb5cfef383fd424d0351f3ddaab7ca2ad; authorized revision 9c9ad71e590aad428d6fdcac23af1ce54ac5fa6065d376ed1f41c11c0823119f; final PONG decision2 revision 11c63e79d25945792e9d8ec16539d28e64e05962e392bf630ab60c53c4f65e29.

## Revise round 1 completed plan

Task revision: sha256:02ce714034a48ce384b6d8c10a628fbf19f6730e55ef192b2e9e6e04f93e644f.
- DONE: README draft ruleset only, operator stops after doctor, mechanical merge restriction deferred to T90b.
- DONE: completion item 4 assigns CompactionDB decision to orchestrator acceptance.
- DONE: independent review correct, formatting/gate pass; one docs commit e2d5c9a3fdae30f6137c5e5fb5cae785691a66fd pushed.
- DONE: final-head CI all passes; final-head Bot wait 18:00:07Z–18:15:08Z reached 15 minutes with no review. Revised RESULT ready for dispatch.

## Result

Revise round 1: PR https://github.com/mryfmo/dotfiles/pull/262, final head e2d5c9a3fdae30f6137c5e5fb5cae785691a66fd on main 8cd66881021c4bffe28d5a3d2ba75aba76e76665. One documentation commit revises the rollout contract; code/tests are unchanged from the previous 778-test run at 507e9c15. Final-head GitHub CI all passes; mergeable=true and mergeable_state=clean. Independent revision review: correct. Prior Bot thread4178600965 is now resolved on GitHub (worker performed no resolution). Final-head Bot wait 2026-10-04T18:00:07Z–18:15:08Z ended at the 15-minute bound; bot: none. No deployment or credential/ruleset provisioning performed.

## Goal
Separate worker GitHub configuration and require current-head approval from a different authenticated login after operator activation.

## Scope
Only task-allowed launcher/manifest renderer, doctor/gate, tests and docs. Seven task-local artifacts; no credentials/accounts/ruleset application/merge. Existing T97 artifacts retained untouched. Branch feat/github-identity-separation from 67451fc66999edded926e92abe4099d3ce21bf87.

## Assumptions
Operator provisions file-backed worker login and stops after make doctor; ruleset design and activation are deferred to T90b. No live worker credential supplied. .agents is read-only and learn index missing; plan/TODO fallback resides here, never committed. UA graph at 940a3a2 is stale against source changes; targeted source searches used, no graph update.

## Design
Manifest path defaults ~/.config/gh-worker and shell-safe rendering. Worker environment selects it and clears token overrides, orchestrator retains default config. Doctor optional before setup, required validation of owned mode0600 token file plus two authenticated distinct logins after setup, no secret output. Integration gate activation needs hosts.yml and effective main rules requiring approval; fail closed on failed verification once file exists. Check PR author, current user and latest current-head approving review. README keeps activation deferred to T90b, with operator setup stopping after doctor; limited guarantee: required approval does not restrict merge actor after approval or isolate credentials from a shared OS user.

## Tests
Tests first for paths/env propagation, doctor absence/security/auth cases, inactive/active gate and stale/dismissed approval. Render/assets, shell lint, focused/full unit tests; no local bats. Independent security review and final CI/Bot.

## Open Questions
Upstream agmsg added-worker tab creation lacks env handoff; orchestrator authorized the narrow subprocess adapter. Official Codex docs have no additional_include key, so supported set.GH_CONFIG_DIR is used for the same authorized worker identity routing (orchestrator notified). Live cross-account scratch merge denial cannot be tested before operator provisioning; document exact operator validation rather than create credentials or attempt a real merge.

## Remaining acceptance/operator work
- Orchestrator: final audit, feedback sweep, integration gate, merge and corrected CompactionDB decision in acceptance. Prior late-P2 thread is already resolved.
- Operator: separate-account provisioning through make doctor only. T90b defines mechanical merge restriction, ruleset activation order and live checks.

## Done
Task revision verified, branch created. Manifest/rendering, worker env handoffs, doctor and gate implemented test-first. README/operator steps, SKILL acceptance step and one integration-rule bullet updated. Independent review correct after fixing submission-order handling; driver/helper fixture verification passed. Render/assets, shfmt/shellcheck, repository Ruff format and Prettier passed.

PR: https://github.com/mryfmo/dotfiles/pull/262
Diff head: a8151c9a65bc893aae4eed6ed0cce5c55732a51a
Updated head before final doctor fix: b99a6f955e3f007ec97dc65c3a018f0aa9a2bfd0 (third update-branch onto boundary main 8cd66881; second was 01ce1acc onto feab6452, first was 3c0cc58b onto T97 6534df0f). Stable patch ID remains 44050f6b826c141f4471ffdc17893a0cef7a18ae.
Local full unit suite: 778 passed; required focused suite: 345 passed.

cost: n/a

## Implementation details and operator follow-up

- Pair/restart: shell-ready check, token-variable removal and shell-quoted GH_CONFIG_DIR export before worker agent start. Orchestrator launch unchanged. Codex CLI set.GH_CONFIG_DIR preserves the path in tool commands under inherit=core; no profile TOML or sandbox/approval/network changes.
- Add-worker: exported Bash herdr adapter exists only in spawn.sh subprocess; tab create adds fixed identity env and pane run prefixes boot with the same selection after shell startup. It creates no extra topology and leaves other herdr calls unchanged. Tests: test_worker_github_pair_env, test_added_worker_github_environment_reaches_boot; existing restart tests cover the shared start path.
- Generator quotes manifest strings with shlex.quote and validates absolute/~/ paths. JSON/TOML quoting protects Codex args, including spaces, quotes, shell metacharacters and hash signs in agmsg spawn-options.
- Doctor reads auth metadata through gh, never prints credentials, validates owned regular mode0600 hosts.yml and active file storage, clears token overrides for both checks, then compares logins case-insensitively. Missing directory is optional, existing invalid configuration is required failure.
- Gate reads effective main branch rules (including applicable organization rules) and paginates reviews. No worker hosts.yml or no required approval yields a notice; malformed responses and API errors after file provisioning fail closed. Latest submitted decisive review must approve exact head by current login, distinct from author. Review IDs only break timestamp ties.
- Independent review found pending reviews can have lower IDs than later-created reviews; corrected submitted_at ordering and regression coverage. Final independent verdict: correct.

Operator provisions a distinct worker account in file storage, retains its hosts.yml privately at mode0600, authenticates the orchestrator default config separately, and stops after make doctor. The approval-only payload remains an unapplied draft. T90b designs the main update restriction with the orchestrator account as sole bypass actor in pull_request mode and its activation order, including boundary-PR coverage. No accounts/tokens/rulesets/live panes were created or changed here. Live merge checks remain deferred and are not claimed as completed.

[memory:decision] T90 selects worker gh credentials through a dedicated GH_CONFIG_DIR and requires a distinct current-head approver in the local integration procedure after provisioning and required-review activation. Required approval blocks unapproved author merges; it does not prevent the author from merging after another account approves, nor isolate credentials among processes sharing an OS user.

Completion item 4: the main-checkout CompactionDB is outside this worker's writable roots. No memory write was attempted and no command is delegated for execution here. The orchestrator records the corrected decision at acceptance; its memory-add output belongs in the acceptance record, not worker validation. T90 delivers credential-role separation and the approval-gated local procedure. The mechanical requirement that only the orchestrator can merge moves to T90b.

Rollout constraint: approval alone permits worker merges after independent approval and blocks orchestrator-authored boundary PRs through self-approval refusal. Do not activate the draft until T90b defines the update restriction, orchestrator bypass actor and activation order.

Bot: none. Bounded wait on diff a8151c9a from 2026-10-04T17:05:45Z to 17:21:12Z; final paginated reviews and inline comments both empty. Wait not repeated for update-branch heads.

CI on 3c0cc58b passed all jobs. On 01ce1acc, tool installation initially failed with upstream chezmoi GitHub release HTTP 500 before tests; retried failed/cancelled unit jobs without source changes. That intermediate head was superseded; final-head CI is green.

Third update-branch imported orchestration-only boundary #263. Original seven untracked T97 artifacts were preserved byte-for-byte under /tmp/t90-prior-t97-artifacts-rl8s53uu before the local fast-forward; the canonical boundary versions now occupy their repository paths. No T90 code changed. Final CI restarted on b99a6f95.

PONG decision2 holds main at 8cd66881 until PR262 acceptance. Task revision verified. Initial 17:21 Bot snapshot was empty; a prior-head review later arrived at 17:23:54. My initial clarification to the orchestrator used the earlier empty snapshot; the subsequent late-review update supersedes it. Base-only heads did not restart the wait.

Previous implementation head: 507e9c159d6ce73998ca70e79ac3951c04f81ff6. Final edge-case review found a doctor P2: an empty XDG_CONFIG_HOME selected ./gh instead of HOME/.config/gh. Added test-first empty/custom XDG subcases and corrected the fallback in one line. All 43 runtime-health tests passed and independent narrow review approved (correct). Full local unit suite and CI rerun passed; Bot wait restarted for this actual code revision, not for base-only merge heads.

## Late Bot finding and acceptance handoff

Codex Bot review on prior head01ce1acc at 2026-10-04T17:23:54Z arrived after the initial bounded wait. P2 thread https://github.com/mryfmo/dotfiles/pull/262#discussion_r4178600965 asks to retire or condition the T97 sandbox exception after provisioning. Independent reviewer assessed it as not-applicable:

not-applicable: Both instructions already require sandbox-first execution and limit the permission-gated fallback to the period before sandbox-readable worker credentials are provisioned. T90 merging does not perform that operator provisioning; README documents login, worker restart and verification. After provisioning, the existing exception no longer applies.

At the previous submission the GitHub thread remained unresolved as required by the worker task, explaining mergeable_state=blocked. At revise-round-1 verification it isResolved=true and mergeable_state=clean; this worker did not resolve it. Orchestrator must still sweep final feedback and run the final audit/integration gate before merging. The edit-scope restriction is not the disposition rationale; the existing conditional wording is.
