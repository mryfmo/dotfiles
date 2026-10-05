---
type: report
id: 20261005_070600
owner: codex-security-dot-a007
status: done
created_at: 2026-10-05T07:06:00+09:00
updated_at: 2026-10-05T00:58:50.738558+00:00
---
# T86 plan / result

Task SHA256: dc73ec191595a158a1eea96a4f1422e470093e81cd83b071bf7a77c6afb36542 (PONG decision6, verified).
PR: https://github.com/mryfmo/dotfiles/pull/271
Head:63a9b107cd327639659b11b87b34276c32c1d3fe (required update-branch integrates main2e65742c, PR269).
Diff head:0f43e161859e6d816d22d7dbefd1c7e3d8ab5128 (fourth authorized fix in round1).

## Goal
Sequential codex exec/resume orchestration with reversible agmsg seat exchange, bounded selected-inbox polling, protected recovery state and private raw evidence.

## Scope
Three source files:158-line Bash launcher,38 fake-CLI tests, README section. Seven uncommitted task artifacts in worker-e for orchestrator transfer. No manifest, herdr-agents, validator, hook, topology, deployment or CompactionDB changes. T85 integrated through567c8d17. Prior accepted task artifacts untouched.

The original150-line target is exceeded by8lines for multi-team restoration that preserves original Codex memberships after partial new-team joins. Task decision2 explicitly says to report restoration-driven overrun rather than remove recovery handling. The hard150-line assertion was removed; wc output is recorded. Orchestrator informed by PONG; independent reviewer accepted the stated exception.

## Assumptions
Report-local plan/TODO is the authorized fallback because .agents is read-only. One active task for this owner. UA graph stale with non-UA source changes; used rg without updating it. No graph-update hook observed. T84 generated environment and T87 live verification gate activation.

Decision5 bounds storage validation: canonical private-state path must not be beneath repository, agmsg skill root or TMPDIR. Managed Codex writable roots exclude this state location; custom writable ancestors can invalidate that assumption and README says so. No attempt to resolve all effective Codex config layers, no permission overrides.

Decision6 explicitly requires all exchanged-team memberships but only selected-team polling. Other inboxes remain unread; README tells workers to route results needed by this invocation through the selected team. This explicit contract supersedes the earlier open scope question.

## Design
Generated model-profiles.env controls orchestrator kind/profile arguments. A private repository-SHA256 directory lock is acquired before identity discovery. Exact-project identities exclude worker seats/aliases. All global registration rows are checked for foreign-project target-name collisions. Existing matching Codex memberships are reused; every exchanged Claude team receives the replacement Codex identity, including a selected team where Codex was not previously registered.

A fresh0700 private run directory contains0600 recovery TSV/context plus raw prompts/finals/console. Snapshot records exchanged Claude rows and original Codex rows before any reset. Project/type-scoped reset preserves other projects/runtimes. Cleanup removes newly added Codex memberships and restores originals, including after partial joins, then restores Claude registrations and both delivery. Failure retains private lock/snapshot. Normal existing-only reuse performs no registration mutation. Codex turn delivery remains configured, documented.

Initial prompt receives herdr-agents --directive, operator task and exact completion instruction. Both initial/resume bodies use stdin;140KiB inbox delivery works. Quiet selected inbox polls every15seconds when empty; idle timeout1800seconds, max turns40. Completion requires the exact final nonblank ORCHESTRATION-DONE line. Hook mode refuses with exit2 until T87 verification.

Repository status contains only turn/timestamps/exit/byte counts/completion/private paths. Raw messages and recovery files never go to repository or agmsg/run. Held public status descriptor closes in child, preventing post-turn symlink redirection. Private context writes rely on the documented protected-state contract. Recovery instructions restore every TSV row, including original Codex memberships, before removing the lock.

## Tests
Final focused38tests pass, including independent execution. ShellCheck, shfmt, Ruff check/format, assets and review gate pass. Full838-test suite passed215.908seconds at diff head; all final merged-head CI checks pass; final Bot wait ended none. No local bats or live seat exchange.

Fourthfix RED reproduced private lock/snapshot and team-exchange failures (38tests,7failures/1error). Obsolete selected-team restriction reproduced separately, removed, and replaced with successful selected-new-membership coverage. Tests cover early private lock, private recovery modes, complete snapshots, all-team registration with selected inbox only, mixed existing memberships, partial new-team join cleanup, inherited earlier140KiB/private-output/path guard/terminal marker/failure tests.

## Review
Crit status reports no review file/server. Independent /root/t97_evidence_review confirmed three prior P2 fixes, found the obsolete selected-team guard, then approved its repair:38tests pass,158lines under reporting exception, Verdict correct. All12resolved JSON records were read before the review gate. Earlier approvals and later findings remain in history; latest decision6 approval is authoritative. No browser Crit, publication or Plan Mode.

## Bot thread dispositions
Worker resolved no threads. Proposed dispositions for all9currently unresolved threads:
- PRRT_kwDOSMyAV86o3y2Y /4179854338: fixed:bb80c63313dfb1c00fb349156cd9153de6bfe200 exact terminal marker.
- PRRT_kwDOSMyAV86o3y2a /4179854340: fixed:c3bd7af000ca2a44d8e6fda0d9926dd3c39969a7 private raw evidence outside checkout.
- PRRT_kwDOSMyAV86o35sF /4179898024: fixed:c3bd7af000ca2a44d8e6fda0d9926dd3c39969a7 generated metadata only, no secret-pattern dependence.
- PRRT_kwDOSMyAV86o35sH /4179898026: fixed:c3bd7af000ca2a44d8e6fda0d9926dd3c39969a7 stdin delivery,140KiB regression.
- PRRT_kwDOSMyAV86o35sJ /4179898029: fixed:c3bd7af000ca2a44d8e6fda0d9926dd3c39969a7 unvalidated hook refusal.
- PRRT_kwDOSMyAV86o35sM /4179898032: fixed:c3bd7af000ca2a44d8e6fda0d9926dd3c39969a7 private raw output under decision5 contract.
- PRRT_kwDOSMyAV86o4F1e /4179976124: fixed:0f43e161859e6d816d22d7dbefd1c7e3d8ab5128 private per-repository lock before identities.
- PRRT_kwDOSMyAV86o4F1g /4179976127: fixed:0f43e161859e6d816d22d7dbefd1c7e3d8ab5128 protected recovery TSV/context.
- PRRT_kwDOSMyAV86o4F1i /4179976130: fixed:0f43e161859e6d816d22d7dbefd1c7e3d8ab5128 replacement joins all exchanged teams; selected-only inbox contract explicit.

Resolved by orchestrator: PRRT_kwDOSMyAV86o3a9U directive dependency implemented in T85 f2d4d709; PRRT_kwDOSMyAV86o3a9T generated kind belongs to T84 and live activation is deferred. Original567c8d17 audit findings fixed by b2e76efc78ecb7dc4023beacb6d55d7833bb6eb8.

Previous c3bd7af0 CI passed; Bot5409022159 arrived00:42:46Z during00:34:57–00:43:14UTC wait, raising the3P2 fixed here. Earlier836full suite passed212.487seconds. Latest-head CI all passes. Final-head Bot wait01:00:34.553558–01:15:35.592976UTC ended bot:none after15minutes; diff-head0f43e161 reviews and top-level comments were also queried afterward and returned no Bot entries. Queries paginate; reactions are not counted.

## Open Questions / T87
Live codex-cli0.160.0 Stop-hook VERIFY exited1 before initialization because runtime home is read-only. Exact probe/output in validation, inconclusive about exec hooks. Task decision1 defers to T87; decision4 refuses hook mode meanwhile. No permission/runtime-home bypass. Orchestrator records CompactionDB decision at acceptance.

## TODO
None for this worker. Orchestrator owns final-head feedback sweep, task audit, thread resolution and integration. T84/T87 activation dependencies remain explicitly deferred.

## Done
Fourthfix implemented and pushed0f43e161; focused tests, review, lints, assets and review gate pass. PR body updated. Seven task artifacts remain uncommitted. Final git fetch confirms0commits behind origin/main2e65742c; final review gate passed after reading12resolved evidence records. PR remains open, mergeable_state=blocked and9threads unresolved per worker contract; proposed fixed dispositions are above. No merge/deployment or live seat exchange.

[memory:decision] Decision6 keeps lock/recovery under protected private state, replaces all exchanged-team registrations and polls only selected-team inbox; original Codex memberships survive cleanup and partial new-team failures. This supersedes the earlier blocked scope report.

cost: n/a

RESULT status=ready_for_review. Latest source diff0f43e161, merged head63a9b107. No remaining worker finding; no P0/P1 on the final head. Bot absence is a bounded-wait result, not review approval.

AGMSG-RESULT ready_for_review delivered via agmsg-dispatch (exit0), confirmed 2026-10-05T01:18:02.290920+00:00.
