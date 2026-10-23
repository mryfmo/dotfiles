---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-install-ppa-resilience-a01 status=pending-integration round=1 pr=454 head=44134e36c167ab57a6ca048b2dd75ff7431b87f8 reason=RESULT-received(precheck-ok,CLEAN,caps-35/80-58/120,red-green-pairs-recorded);chain-queued-after-PR-378-on-the-single-review-worktree;your-question-PONG(handoff-R8-3)-is-relayed-to-the-operator-as-J-F-and-counted-in-INV-6 next_action=hold:no-worker-action-until-accepted-or-revise read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-install-ppa-resilience-a01 status=revise pr=454 previous_head=44134e36c167ab57a6ca048b2dd75ff7431b87f8 round=2 amendment=3 task_file=.orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md previous_task_sha256=45fb80f66c9ca36ef5dc3595d516404b64b6060fab4bd2a2c3b7e3174a83488f task_sha256=bc6a455f69646a15c4042503e775e93f359171ee535f3fdbff8e501a02a8a7b5 reason=task-level-audit-of-44134e36(.orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-44134e3.md.last.md):incorrect,five-P2-no-P1;amendment-3(anchored-by-a011-round-5):Item-3-moves-the-ghostty-step-into-home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl(guard-of-run_after_05-client-install-zed)-and-removes-the-include-from-the-misc-run_once_-script,installer-idempotent;Item-1-outage-detector:an-exit-0-apt-get-update-reporting-a-failed-PPA-index-is-an-outage,a-fetch-failure-from-another-host-stays-fatal;validation.md-verbatim(JSON-stays-JSON,every-command-with-output,the-lint-red-run-included);main-moved-to-7b21659e:rebase-or-merge-main-before-the-push check=tests/install/ubuntu/client/ghostty.bats::an_apt-get_update_that_reports_a_failed_PPA_index_without_a_non-zero_exit_is_an_outage check=tests/install/ubuntu/client/ghostty.bats::a_fetch_failure_from_another_host_stays_fatal_even_when_the_PPA_also_failed check=tests/install/ubuntu/client/ghostty.bats::the_ghostty_step_is_a_guarded_run_after__script_and_the_misc_run_once__script_no_longer_includes_it next_action=round-2:write-.orchestration/dotfiles-T133-install-ppa-resilience-a01/revise.yaml(previous_head,checks),red-then-green-per-check,push,CI,Bot-wait,RESULT-round=2 read_at=read"
  ],
  "format": 1,
  "head": "44134e36c167ab57a6ca048b2dd75ff7431b87f8",
  "ledger": [],
  "pr": 454,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-install-ppa-resilience-a01"
}
---
# Acceptance: dotfiles-T133-install-ppa-resilience-a01

Essential remedy for the Launchpad PPA dependence of the required check `test (ubuntu-24.04, client)` (D-024-67, C-132). Text authored by the orchestrator (security: false, no C-80), anchored by `dotfiles-T133-install-ppa-resilience-a01-review-a01` (a011): round 1 reject (the live ghostty test still asserted dpkg success), round 2 reject (a separate InRelease probe misjudges a pool-only outage), round 3 accept at sha256 45fb80f66c9ca36ef5dc3595d516404b64b6060fab4bd2a2c3b7e3174a83488f (62 lines; the live test uses the installer's own retry line as the oracle). Dispatched 2026-10-21T22:29Z to claude-standard-dot-a008 (worker-f) on a fresh branch from origin/main.

## Owned by dotfiles-T133-install-ppa-resilience-a01-followup-a01 (advisory; rows id<TAB>class)

local:45fb80f:1	oracle-is-sut-output

Row 1 (P2, the anchor review): the live test's oracle is the installer's own retry line, so an installer that wrongly printed it with the PPA reachable would pass the live test; the two fake-based cases pin the exact failure path, and the owner follow-up may add an independent oracle (an apt-cache policy probe after the run).

## Counters (INV-6)

amendments=0 revises=0 questions=0 at dispatch.
dispatch: [2026-10-22T01:30:41Z] claude-deep-dot → claude-standard-dot-a008: AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-install-ppa-resilience-a01 status=pending-integration round=1 pr=454 head=44134e36 (bus row ○ read; recorded by hand because the dispatch.sh run that sent it was stopped during its slow post-send bus read; the later re-send with BUS_READ_WINDOW=40 added no row)
local:44134e3:1	advisory-p2
local-finding: 44134e3:1 not-applicable:advisory P2 owned by dotfiles-T133-install-ppa-resilience-a01-followup-a01 (- [P2] Detect failed index downloads when apt exits zero — install/ubuntu/client/ghostty.sh:52-53); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md (02f669d1042aa9137bffaa1f3cb5c5184372a19173b7610e1c28661bc658db0d)
local:44134e3:2	advisory-p2
local-finding: 44134e3:2 not-applicable:advisory P2 owned by dotfiles-T133-install-ppa-resilience-a01-followup-a01 (- [P2] Keep skipped installations eligible for the next apply — install/ubuntu/client/ghostty.sh:68-70); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md (02f669d1042aa9137bffaa1f3cb5c5184372a19173b7610e1c28661bc658db0d)
local:44134e3:3	advisory-p2
local-finding: 44134e3:3 not-applicable:advisory P2 owned by dotfiles-T133-install-ppa-resilience-a01-followup-a01 (- [P2] Preserve non-PPA errors in mixed apt failures — install/ubuntu/client/ghostty.sh:53-53); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md (02f669d1042aa9137bffaa1f3cb5c5184372a19173b7610e1c28661bc658db0d)
- 2026-10-22T02:32Z: chain of 44134e36 complete (sweep 6 items, gaps 0; audit `…-audit-44134e3.md.last.md` Verdict incorrect, five P2, no P0/P1: apt-get update exit 0 with a failed index; a mixed fetch failure turned into success; no retry after a skip (run_once_ records completion); the record deferred in-scope P2 instead of a revise round; validation.md not verbatim). Operator answered J-I (D-024-74): amendment 3 of the text (run_after_06 template guarded like the zed template, idempotent installer, tightened outage detector, three fixtures, verbatim evidence, caps 110/160 in `## Check`) anchored by a011 (round 4 reject: caps sentence placement, unguarded template; round 5 accept at sha bc6a455f69646a15c4042503e775e93f359171ee535f3fdbff8e501a02a8a7b5); ACCEPTANCE status=revise round=2 sent to a008 with three check= selectors and the verbatim-evidence requirement (bus row after 2026-10-22T02:32Z, hand line). The audit's seven findings are dispositioned by this round: 1-3 and 5 by the checks, 4 by this revise itself (plan 020 step 4). counters before the send (`scripts/regime-counters.sh dotfiles-T133-install-ppa-resilience-a01`, 2026-10-22T02:32Z): task=dotfiles-T133-install-ppa-resilience-a01 tasks=1 amendments=0 questions=1 results=1 withdrawn=0 revises=0 first_result_head=44134e36c167ab57a6ca048b2dd75ff7431b87f8 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-21T22:29:04Z..2026-10-22T01: / detail: pr=invalid authors=claude-deep-dot tasks=01a16095-0f80-73e6-8cb8-39a76b87ec61 results=01a16132-e5c0-7b3a-8fda-ce174e72538c questions=01a1612e-6568-77ee-8696-60f125766bdf withdrawn=- bot_heads=- source=live

