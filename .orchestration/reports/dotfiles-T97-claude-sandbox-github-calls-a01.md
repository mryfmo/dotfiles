# T97 — root cause reproduced; safe settings-only fix unavailable

status: blocked
owner: codex-security-dot-a007
cost: n/a

## Goal / Scope
Make Claude sandbox GitHub calls work, using only evidence-backed changes in the dispatched allowlist. Worker-e only. Task revision 1 SHA256 verified: ac076fab47928f50a080a9a256dbd62f0eee8ed6a93eac4ada363d784baa3a38. The SKILL edit remains dependent on PR 253 merging.

## Outcome
Claude Code 2.1.288 scratch express sessions reproduce the root cause. `gh api user --jq .login` and `gh pr view 253 --json url,state` each exit 1 with HTTP 401. `git fetch origin` and `git push --dry-run origin HEAD` succeed without an unsandboxed retry. The task's premise that all four calls fail is not true on this Linux host.

Socket-only strace proves that gh's `socket(AF_UNIX, ...)` returns `EPERM` inside Claude's sandbox. The parent Codex execution successfully opens that socket, connects to `/run/user/1000/bus`, and authenticates using the keyring. Scratch `gh auth status` reports an invalid default token, while the parent reports a valid keyring token. No token values were printed or copied. Neither context has GH_TOKEN or GITHUB_TOKEN set.

This is not a missing GitHub domain or missing read permission on hosts.yml: GitHub returns an authenticated-endpoint 401 over an established proxy connection, while credential lookup fails at socket creation. Mount/network namespace IDs differ between parent and scratch, and the scratch has two seccomp filters rather than one. No `<sandbox_violations>` block was emitted; the syscall denial is the direct evidence.

## Why blocked
The required four-command success cannot be delivered through the allowed manifest-only repair while preserving the existing socket restriction. Linux `allowUnixSockets` cannot permit a single path. `allowAllUnixSockets` removes the protection for all local services and is explicitly excluded by the manifest's T44 security decision. Adding a D-Bus path or more GitHub domains would not fix AF_UNIX creation denial. No such ineffective or broad change was made.

A different, operator-provisioned authentication mechanism that works within the sandbox would require a new scope and its own secret-handling design. This worker did not export a keyring token into the scratch environment, write a plaintext token file, relay a D-Bus socket, turn off the filter, change hooks/permissions, or retry outside Claude's sandbox. The task's explicitly mentioned residual auto-mode/domain case was not observed; the residual here is keyring access.

## Concrete proposed next action
Re-task to document this demonstrated Linux/keyring limit, or task a separately scoped authentication-provisioning design. Suggested replacement for the blanket GitHub exception, once PR 253 merges:

> Run git fetch/push and gh inside the sandbox first. On Linux, gh backed by the host keyring can fail with HTTP 401 because AF_UNIX socket creation is denied; allowUnixSockets cannot grant a path-specific exception there. Workers report that credential-access blocker and wait for re-tasking. Do not add GitHub domains or enable allowAllUnixSockets to work around it. A gh call with separately provisioned sandbox-compatible authentication must be verified before declaring the limit retired. Git fetch and push dry-run succeeded in the T97 reproduction and need no blanket unsandboxed exception.

This is a proposed sentence, not an implemented policy change or approval for unsandboxed calls. Its acceptance criteria would differ from the current four-success requirement.

## Plan / TODO
- Await re-tasking on the demonstrated keyring limitation.
- If a documentation-only residual is accepted, wait for PR 253 merge, then amend only the authorized sentence and matching rule and run the requested validations/review/PR workflow.
- Four-operation success remains unfulfilled for gh until a supported credential source is supplied within the accepted trust boundary.

## Done
- Read task and skills, verified both dispatched task revisions, checked gh/Claude configuration without secrets.
- Initial branch command failed on shared config access. Orchestrator re-tasked; `git switch fix/claude-sandbox-github-calls` recovered the existing branch, exit 0, with no reset required.
- Ran three authorized scratch Claude express sessions with normal settings and no permission override; saved tool calls and raw outputs in validation.
- Independently compared the parent keyring and socket behavior.
- Checked the upstream implementation and existing README; both already explain the Linux Unix-socket limitation.
- Wrote the five permitted artifacts in worker-e.

## Assumptions / Design / Tests
No learn index exists in worker-e or the main checkout. The knowledge graph was consulted and stale, so source reads were used. `.agents` is read-only for this session, hence the plan/todo live here. Use only MODEL_PROFILE_EXPRESS_CLAUDE_ARGS from the generated manifest profile file for scratch sessions.

No product file was edited, no regression code was added, and no build/unit/bats tests were run. A fix or PR that claims all calls succeed would be unsupported. No commit or PR was created. No settings/render change means no user-visible permission change.

## References
- PR dependency (OPEN at observation): https://github.com/mryfmo/dotfiles/pull/253
- https://github.com/anthropics/sandbox-runtime/blob/main/src/sandbox/linux-sandbox-utils.ts
- https://code.claude.com/docs/en/sandboxing

gh was used first. Web was needed to locate the current primary documentation and canonical upstream repository after a guessed source path returned 404.

## Durable finding / CompactionDB handoff
[memory:failure] dotfiles-T97: On Linux with Claude Code 2.1.288, gh keyring authentication fails in sandboxed Bash because AF_UNIX socket creation returns EPERM before D-Bus keyring lookup. REST/GraphQL calls then return HTTP 401. Git fetch and SSH push dry-run succeeded with existing domains; adding domains is not a fix, and the Linux path-specific allowUnixSockets setting cannot restore keyring access.

The main checkout is outside this worker's writable roots. No memory record was created; the orchestrator can run this unexecuted handoff command after accepting the evidence:

```sh
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project 'dotfiles-T97: Preserve the Linux Unix-socket restriction. Claude 2.1.288 gh keyring authentication returns HTTP 401 after AF_UNIX creation is denied; git fetch and push dry-run succeed. Do not add domains or enable all Unix sockets to mask this credential-access limit.'
```

No plan-mode Crit session was started. No Understand-Anything auto-update hook was observed. Acceptance authority remains with the orchestrator.

Completion gate remains pending: raw evidence makes the five artifacts exceed the broad-diff threshold; `make require-crit-review` exited 2. `crit status --json` reports no review data and no daemon. The dispatched allowlist contains no additional review JSON path. No approval was fabricated or bypass requested; this is a blocked diagnosis report, not a completed/approved PR.

## Revision 2 — accepted investigation, documentation-only continuation

Task SHA256: 900ba93da416a8efaf6554fa763eae0cf2dedad462f993d5df4b4c54b7238704. The orchestrator accepted the reproduction and moved worker credential provisioning to T90. The earlier blocked diagnosis above is preserved as historical evidence. Current status: waiting for PR 253 to merge, then active documentation work.

Plan: preserve all five investigation artifacts; replace only the specified SKILL step-4 sentence and matching rule bullet after PR 253 merges; run the existing validation commands, independent agent review, create an English PR, follow CI and final-head Codex Bot feedback, and send RESULT. No sandbox setting, generated config or new test changes are planned. Existing docs validation suffices for this narrowly prescribed sentence edit.

TODO: dependency merge, sentence edit, validation/review, PR/CI/Bot, final RESULT. Done: revision hash verified; extra review evidence paths requested from orchestrator because Crit has no data. CompactionDB finding will be recorded by the orchestrator under the revised task.

## Go-ahead — implementation resumed

Verified task revision d91836c1b7b78fede3796ffe927024f44766db459c6825bd05b8b73a1645f461 and PR 253 merge at 04bce61b47b15d6f748abdce05bfdc5a8943bd98. Created `docs/claude-sandbox-gh-keyring-limit` from that origin/main with --no-track. The latest instruction explicitly includes the rule bullet as well as Worker Playbook step 4.

Current TODO: edit the two clauses; run requested render/assets/unit validation; obtain final independent review and worker receipt; commit/push product docs and create PR; complete CI and bounded final-head Bot wait; append final status and send RESULT. Evidence-only review already approved the five preserved artifacts with no actionable findings.

## Product change submitted

PR: https://github.com/mryfmo/dotfiles/pull/258
Head: 8ffa554738c6f8b524f33787332a31337e935122
Base: 04bce61b47b15d6f748abdce05bfdc5a8943bd98
Branch: docs/claude-sandbox-gh-keyring-limit

Both prescribed clauses are implemented. The PR contains only the SKILL and matching rule prose; artifacts remain in worker-e for orchestrator transfer. Render check, asset validation (regime-hygiene warnings), Prettier, diff check and independent review passed. Worker receipt gate passed. Unit suite and GitHub CI are currently running; final-head Bot wait follows. No runtime settings, credentials, hooks or permissions changed.

## Final RESULT — ready for orchestrator review

Current status: ready_for_review. This section supersedes the historical blocked/in-progress states above; all earlier raw investigation artifacts are preserved as requested.

- PR: https://github.com/mryfmo/dotfiles/pull/258
- Head: 8ffa554738c6f8b524f33787332a31337e935122
- Base: 04bce61b47b15d6f748abdce05bfdc5a8943bd98, current at final check.
- Product diff: exactly two prescribed prose changes, SKILL step 4 and the matching rule bullet. Runtime sandbox settings, credentials, hooks and permissions unchanged.
- Validation: render-check, validate-agent-assets, all 787 unit tests, diff check and Prettier pass. GitHub CI all pass on this head; gh pr checks --watch exited 0.
- Independent review: evidence, two-file product diff, and subsequent Bot finding assessment all reviewed by t97_evidence_review. Worker-side JSON/receipt files are in the permitted -worker-crit.json / -worker-review-receipt.md paths.
- Bot: final-head Codex review 5406686942, submitted 2026-10-04T14:38:11Z, found on first post-CI query. No P0/P1. One P2, detailed below. No additional Bot wait needed because an actual final-head review exists.
- PR description updated to the full final implementation and validation state, with requested attribution footer.
- Cost: n/a. No Crit plan server was started; no plan-mode-used marker applies.

### All unresolved review threads

`PRRT_kwDOSMyAV86ozh63` (comment `4178090986`, P2, SKILL line 170):

`not-applicable: Claude 2.1.288 runtime mountinfo shows shared Git objects, refs, logs and worker-e metadata mounted writable; test -w confirms access. The finding infers effective permissions solely from launcher/config entries, contradicting observed runtime grants. Shared Git config remains read-only; the branch workflow uses --no-track.`

This is a **proposed** disposition for orchestrator acceptance. The worker resolved no GitHub thread. The read-only check establishes runtime grants in this environment, not a successful fetch of new objects or every future Git operation. The full mount/tool evidence and independent assessment are in validation. GitHub mergeable_state remains `blocked` with that unresolved thread despite green CI.

### Completion / handoff

Worker TODO: none under the documentation-only scope. Done: dependency merge verified, exact text applied, local checks and independent review, PR/push, CI, final-head Bot review, proposed disposition and evidence. Orchestrator next: transfer all seven worker-e artifacts, record the accepted CompactionDB finding as directed in re-task 2, sweep final feedback and perform its task audit/acceptance/integration gate, then disposition/resolve the thread and decide merge. T90 owns credential provisioning. No PR merge or acceptance was performed by this worker.

## Acceptance revise round 1 — in progress

Verified task SHA256 db5c98cf7004ab5bcba5e8fdb2bce81d608e420307f6a27ee9b393cbbe4dc1c0. The orchestrator dispositions the first-head Bot P2 as not-applicable based on its own Claude-seat evidence. It requests two exact wording corrections: include git push whose credential helper is gh in the temporary permission-gated exception, and remove the duplicate blocked-PONG sentence in the SKILL.

The initial SSH push dry-run did not establish that HTTPS pushes using gh credentials work. The revision reflects the orchestrator's T72/T76/T95 push evidence while keeping public-remote fetch inside the sandbox.

TODO: one commit changing both docs; focused docs tests; independent review/receipt; push; update PR description; final-head CI/Bot and RESULT. No credential or runtime setting changes.

## Revise round 1 progress — new head CI green

The requested single correction commit is 68e19ef775d5906e49de0a75d214a0a4a5f3f909. Both prose corrections are in PR258 and its description now explains the full gh/HTTPS-push credential-helper residual. Six docs tests, Prettier, diff check, independent review and the worker gate pass. New-head CI checks all pass. A bounded final-head Codex Bot wait started after CI at 2026-10-04T15:08:33Z; the first query had no review or inline finding on that head. Completion remains pending that wait and final thread/base checks.

## Main advanced during revision validation

The 68e19ef head passed CI and the full 15-minute Bot wait found no new-head review. Main then advanced to 40993f2. Per the task, gh pr update-branch succeeded and the local branch fast-forwarded to b8f293ef608a1ff48b36b44a55004d81484dc8cf; the PR still changes only the two prescribed docs. Current TODO: updated-head CI and Bot wait, final base/thread checks, receipt and RESULT. Earlier ready-for-review sections are historical.

## Second main advance — current active TODO

b8f293ef passed all CI and a full 15-minute Bot wait with none. Final checks found main f6320f37. Required update-branch succeeded; head is now 5b6b0d9f89049eff0efbdc4699c425f711e58557. Product diff is still two docs only. TODO: CI/Bot on this updated head, final checks, final RESULT. Orchestrator asked to coordinate main integration to avoid repeatedly invalidating final-head checks.

## Round 1 addendum — final completion condition

Verified task revision dc1983079856e574371933204d87913ffbe9db23db70b1a50c4f71fbdd335c18. The orchestrator explicitly waives repeated Bot waits on update-branch-only heads and holds main integration until PR 258. The required report marker is bot=none-on-68e19ef7, the unchanged diff head whose complete wait already elapsed. Current TODO: CI on 5b6b0d9f, final state/thread checks and RESULT. No further Bot wait will be started for this merge-only head.

## New final-head Bot finding — needs task decision

All CI on 5b6b0d9f passed, main is f6320f37, but actual final-head Bot review 5407013778 arrived at 2026-10-04T15:56:13Z. New P2 comment 4178339453 / thread PRRT_kwDOSMyAV86o0JBE correctly identifies private HTTPS fetch authentication via gh; independent reviewer confirms it is valid. The installed docs have no public-only scope, and public fetch evidence does not disprove this. Prior Bot wait-none marker applies only to 68e19ef7. No not-applicable disposition is proposed for the new P2. Current TODO: obtain orchestrator scope revision for the exact prescribed sentence, implement correction if directed, validate/CI/Bot and RESULT. PONG sent with evidence; GitHub thread remains unresolved.

## Final revised RESULT — ready_for_review

This section supersedes earlier pending/blocked/ready states. Latest task revision: b8c92fbcaf7aa91e01acda3eba7a767d06fdb3a802f70879341a37809386e862, including both round-1 addenda.

- PR: https://github.com/mryfmo/dotfiles/pull/258
- Final head: 5b6b0d9f89049eff0efbdc4699c425f711e58557; base/current main: f6320f37d3835b37204584e00eb67d0bb41bf577.
- Correction commit: 68e19ef775d5906e49de0a75d214a0a4a5f3f909. Both prescribed files include gh-backed git push in the temporary exception; SKILL keeps only the final blocked-PONG sentence. Subsequent commits only incorporate main. Product diff remains two documentation files; runtime settings, permissions, hooks and credentials unchanged.
- Validation: six docs tests, Prettier, diff check and independent wording review pass. All final-head CI checks pass. Initial render/assets checks and 787 tests passed before the wording revision; no claim they were locally rerun on this final head. Worker gate passes with the latest addressed receipt after reading the JSON evidence.
- bot=none-on-68e19ef7: the complete 15-minute wait elapsed on that diff head. b8f293ef also completed its wait. Per addendum 1, no repeated wait was required on 5b6b0d9f; final inspection nevertheless found actual Bot review 5407013778 on it, submitted 2026-10-04T15:56:13Z.
- All unresolved threads: none. Both PRRT_kwDOSMyAV86ozh63 (4178090986) and PRRT_kwDOSMyAV86o0JBE (4178339453) were dispositioned not-applicable and resolved by the orchestrator. The worker resolved neither.
- Material limitation: the new private HTTPS fetch P2 is technically valid, independently confirmed. The orchestrator's addendum 2 excludes private remotes from this public-repository worker regime and directs no text change. This is a scope decision, not a technical fix or withdrawal of the independent finding. T90 owns credential provisioning.
- All seven requested artifacts remain in worker-e for orchestrator transfer, outside the PR. Earlier raw evidence is preserved. CompactionDB finding recording remains the orchestrator's responsibility under re-task 2; no memory write is claimed here.
- No Crit plan server/session was started. No plan-mode-used marker applies. No PR merge or acceptance performed by this worker.

Worker TODO: none under latest scope. Orchestrator next: transfer seven artifacts, record the CompactionDB finding, run its final feedback/audit/acceptance/integration workflow, and decide merge.

cost: n/a

## Revise round 2 — active

Task revision 8364021c54a3b749b687e8c68f7152602302c69f2321871c66008b2a102f0a2a verified. The task audit agrees with the independent private-fetch P2: installed global rules cannot be limited by this repository's visibility. The previous orchestrator scope disposition is superseded. Plan/TODO: replace the exact phrase in both docs to include authenticated git fetch, run docs tests and Prettier, obtain independent review and update evidence, commit/push once, wait for final-head CI, inspect feedback and send RESULT without another Bot wait (explicit round-2 direction). Main remains held for PR258.

## Round 2 pushed — CI pending

Correction commit/head: efe6735e4542029b1357d27d1e47b63a57273ed4. Exact phrase applied in both docs; initial sandbox attempt still required. Six existing docs tests passed before and after, Prettier and diff check passed, and independent reviewer confirmed the private HTTPS fetch P2 fixed with no new findings. JSON/receipt updated and worker gate passed. PR description now describes authenticated fetch and supersedes the earlier scope dismissal. Current TODO: final-head CI, feedback/base checks, final artifacts and RESULT. No additional timed Bot wait per explicit round-2 instruction.

## Round 2 CI retry

Ubuntu24 client Ghostty test failed on an external Launchpad HTTP IncompleteRead; the same efe6735e failed job was rerun once with gh run rerun 37215840356 --job 111476070040. Raw failure is in validation. Current TODO remains final CI, feedback/state checks and RESULT.

## Final round 2 RESULT — ready_for_review

This section supersedes all earlier final/pending/scope-disposition sections. Task revision 8364021c54a3b749b687e8c68f7152602302c69f2321871c66008b2a102f0a2a.

- PR: https://github.com/mryfmo/dotfiles/pull/258
- Final head/correction: efe6735e4542029b1357d27d1e47b63a57273ed4. Base/current main: f6320f37d3835b37204584e00eb67d0bb41bf577. mergeable_state: clean.
- One phrase changed in both prescribed documents, adding authenticated git fetch to the gh/git push permission-gated exception. Sandbox-first requirement and adjacent restrictions preserved. No runtime, permissions, hooks or credential changes.
- Private HTTPS fetch P2 comment4178339453 / audit finding1: fixed:efe6735e4542029b1357d27d1e47b63a57273ed4. The global installed scope invalidates the prior public-repository dismissal; independent reviewer confirms the correction and no new issues. The underlying keyring limitation remains for T90; this commit fixes its policy coverage.
- All six docs tests passed before and after, Prettier/diff check and worker review gate pass. All final-head CI checks pass. Both Ubuntu client Ghostty jobs initially failed on Launchpad IncompleteRead; each passed a targeted rerun at the unchanged head. Raw failures and retry evidence preserved. No local bats run.
- Final-head feedback queried after CI: no new review or top-level inline finding. No unresolved threads; both existing threads were resolved by orchestrator. No new timed Bot wait per explicit round-2 dispatch. The prior bot=none-on-68e19ef7 marker is historical and is not claimed as a wait on this head.
- Initial render/assets/787-test results remain historical, not represented as locally rerun on this head. PR description updated to the final authenticated-fetch implementation and actual validation history.
- Seven artifacts remain untracked in worker-e for transfer. Existing evidence preserved; worker receipt latest outcome approved and cites round-2 independent review. No Crit plan session/server used. No merge, acceptance or CompactionDB write performed here.

Worker TODO: none under round-2 scope. Orchestrator next: transfer artifacts, sweep final feedback with the private-fetch finding fixed at efe6735e, audit this new head, record CompactionDB finding and run acceptance/integration gates.

cost: n/a
