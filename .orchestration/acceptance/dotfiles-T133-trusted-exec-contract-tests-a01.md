---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-trusted-exec-contract-tests-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md task_sha256=dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c deadline=none done_signal=AGMSG-RESULT note=a011:test-only-helper-of-design-5.14-item-7(tests/unit/trusted_exec_contract.py-and-its-own-tests;no-production-consumer-yet);fresh-branch-from-origin/main;keep-tools/chain-review-scripts-followup-a06-untouched-for-its-pending-integration;security:false;the-Checks-block-at-the-end-carries-the-counters"
  ],
  "format": 1,
  "head": "a561e640c59debc7e99eec5535acd65f139077e4",
  "ledger": [
    {
      "class": "happy-path-closing-test",
      "id": "audit:9545e59:1"
    },
    {
      "class": "evidence",
      "id": "audit:9545e59:2"
    },
    {
      "class": "evidence",
      "id": "audit:9545e59:3"
    },
    {
      "class": "evidence",
      "id": "audit:9545e59:4"
    },
    {
      "class": "acceptance-dispositions",
      "id": "audit:9545e59:5"
    },
    {
      "class": "missing-owner-task",
      "id": "audit:9545e59:6"
    },
    {
      "class": "escape-detection-gap",
      "id": "audit:a561e64:1"
    },
    {
      "class": "escape-detection-gap",
      "id": "audit:a561e64:2"
    },
    {
      "class": "unhashed-text-change",
      "id": "audit:a561e64:3"
    },
    {
      "class": "evidence-placeholders",
      "id": "audit:a561e64:4"
    },
    {
      "class": "disposition-label",
      "id": "audit:a561e64:5"
    }
  ],
  "pr": 436,
  "replans": {
    "evidence": {
      "design": "the worker writes commands from a command log (the a06 lineage's `*-commands.json` plus `measure.md` pattern) rather than by hand, and the orchestrator's evidence check refuses a validation whose recorded commands contain unexpanded `$VAR` tokens or whose base/candidate counts disagree with their claims (`result-evidence-check.sh`, orchestrator-side)",
      "implementation": "the records-only commit of amendment 1 replaces the placeholders in this lineage; the check is an item of `dotfiles-T133-result-precheck-followup-a01` (D-024-46)",
      "specification": "every recorded command in report.md and validation.md is the literal command that ran, with its exit code and output, and every claim about a run names its log; no shell variable, placeholder or summary stands in for a command",
      "verification": "the task-level audit of the final head reports no evidence-class finding, and the evidence check passes on that head."
    }
  },
  "searches": [
    {
      "class": "evidence",
      "records": [
        "M-20261012-3.md",
        "M-20261014-09.md",
        "M-20261014-10.md",
        "M-20261020-04-result-claims-against-own-counts.md"
      ]
    }
  ],
  "task": "dotfiles-T133-trusted-exec-contract-tests-a01"
}
---

# Acceptance record: dotfiles-T133-trusted-exec-contract-tests-a01

Design 5.14 item 7 shared test helper (test-only; D-024-30 by-reference text). Authored by the review profile (`p-tec-author-prompt.md` -> `redesign/p-tec.md`), 197 lines, 3 files, checker OK, no C-80 (security: false).

- 2026-10-19T23:29:36Z: dispatched to a011 (worker-d); text sha256 dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c.
- 2026-10-20T01:48:10Z: a011 RESULT round 1 `status=ready_for_review`: PR #436 (draft) head 25dd01e582f5bfa867e4cc9d306e03e529afe607, code head f4eed1cc, base ba318e53, task_copy dd754911…; tests/unit/trusted_exec_contract.py 242/250 lines, tests/unit/test_trusted_exec_contract.py 324/350; nine selectors (each probe detects its condition; shim, hostile git, worker root, swapped file, sanitised environment, trusted parent, passwd home per platform, cleanup after an exception); red at 755d9002 then green at f4eed1cc under uv offline on the exact python 3.15.0 and under the seat's default 3.10; per-probe red on a non-compliant stub then green; 12 wrong implementations each red; the case-alias case ran on APFS and skips on Linux CI with the measured reason; the real dscl was not run (exit 70 inside the sandbox; mocked); the worker's own review: 5 P2 fixed in one worker-side round (f4eed1cc). Adversarial check next: CI on 25dd01e5, caps by numstat in the chain, the owner text written (C-51), the PR marked ready.
- 2026-10-20T01:53:16Z: measured: 7 required checks, the canary and regime pass on 25dd01e5; GitGuardian (non-required) reports one `Generic Password` in commit 755d9002 at test_trusted_exec_contract.py:299: the synthetic passwd entry `name:x:uid:20:Probe:~:/bin/bash` of the getent mock, no credential (refutation in 436-extra.tsv with the git show evidence); PR marked ready; ACCEPTANCE pending-integration sent; owner text trusted-exec-contract-tests-followup-a01 written (checker OK); chain next.
- 2026-10-20T02:1xZ: the chain on #436: the base had moved (ba318e53 -> 118daafa), update-branched to 9545e59f; the chain refused at the required-checks step (rc 12: a required check failed on the new head); the failing job read next.


## Owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:9545e59:1	advisory-p2
local-finding: 9545e59:1 not-applicable:advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (- [P2] Give worker-root writes a distinct timestamp baseline — tests/unit/trusted_exec_contract.py:109-111); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md (0c36290491e31ae2ccdbba12fb5321e3c1300c3951838d90b07756bfc6c5a65d)
- 2026-10-20T02:29:42Z: the chain on 9545e59f: every required check passes; the sweep found the GitGuardian check-run of the new head (a new run id, the same synthetic-passwd finding) and one CI download-retry annotation without rows; both dispositioned not-applicable with evidence; chain re-run.
- 2026-10-20T02:36:37Z: the chain on 9545e59f: sweep 0 gaps; task-level audit `…-audit-9545e59.md` `Verdict: incorrect`: P2 implementation (a same-length overwrite evades assert_untouched: INV-3 violated); P2 evidence (mutation M16 never ran; the twelve-mutation claim invalid); P3 evidence x2 (the 3.10 claim unsupported; the macOS CI claim wrong: test.yaml:119 skips unit tests for a Python-only diff); P2 orchestration (the known timestamp defect was deferred although small: a bounded revise is required); P3 orchestration (the owner text described PR #430: the orchestrator's clone from the assets template, fixed now). Plus the orchestrator's measured finding: passwd_home() calls dscl, which fails inside both seat sandboxes. Revise round 1 to a011 (= the second and last worker round under the inherited clause) with four selectors; the owner text corrected.
audit:9545e59:1	happy-path-closing-test
audit:9545e59:2	evidence
audit:9545e59:3	evidence
audit:9545e59:4	evidence
audit:9545e59:5	acceptance-dispositions
audit:9545e59:6	missing-owner-task
- 2026-10-20T03:27:48Z: a011 RESULT `round=1 revise=1`: head a2f47445a0d1d42802ab1afe958e21cd485118f6 (code 7d3ecd4f; fast-forward from 9545e59f; four commits: tests red, fix, the non-absolute-home case, the P3 fixes); (1) same-length overwrite detected (fixed past mtime + whole-content compare from the same inode and mode, access time put back), red at bb539aa7 then green; (2) 17 mutation blocks each red with unique anchors (M16 anchored on the runner check=False call); (3) the report states only pasted output (3.10.22 by absolute path: 10 OK; macOS CI skips the unit suite for this diff); (4) passwd_home() reads pwd.getpwuid first, dscl/getent only as a cross-check when they run (red at bb539aa7 in 6 subtests, green at 7d3ecd4f; live: dscl exit 70, passwd_home = the getpwuid home); caps 247/250 and 350/350 (reached exactly); the worker's own review of the round: correct, 5 P3 fixed; declared follow-ups (older worker-root gaps: sibling file, output read, rename-away-and-back, identical bytes with mtime put back; the newline half of the home check; one unexplained failure in a mutant run). ACCEPTANCE pending-integration at 2026-10-20T03:29:06Z; chain next (the GitGuardian run id changes per head; the sweep names it).
- 2026-10-20T03:42:21Z: chain on the update-branched head b3c50768 stopped at the sweep (rc=14, 3 gaps). (1) `regime` run 39364553764 failed: `regime-ci: … task-copy: .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/task.md differs from the base's dispatched .orchestration/tasks/…` — root cause: boundary 25 (#435, committed 2026-10-20T00:19:29Z) carried a snapshot of the task text taken before its dispatch line was pasted (dispatch 2026-10-19T23:29:38Z, task_sha256 dd754911…; the PR copy and the local text both equal it; main's copy lacks the one `dispatch to a011 …` line inside the Checks block); the same staleness holds for loop-limits-a01 (dispatched 00:55:43Z after the boundary commit). Proper state: main's tracked text equals the dispatched bytes, which regime-ci treats as the policy. Fix: records PR #438 (`records/sync-dispatched-texts-26`, head 8bf7e6ac) replaces both texts with the dispatched bytes; after its merge (operator approval per design 5.14 item 8, D-024-33) #436 takes the new base with `gh pr update-branch`, then CI, sweep and chain again. (2) GitGuardian check run 118438279783 re-reports the synthetic passwd fixture (four test-file occurrences and one in result.txt): refuted in `436-extra.tsv`. (3) the regime job's `Process completed with exit code 1` annotation is the same failure as (1). Mechanism: the boundary procedure must verify, before pushing, that every in-flight task text it carries equals the latest `task_sha256` dispatched on the bus (M-20261020-02 to be written with the boundary-26 preparation).
- 2026-10-20T04:39Z: PR #438 extended (head c58cf432) with the lint a04 and a05-checker texts; CI rerunning; the operator's approval is still the pending step; then update-branch #436.
- 2026-10-20T05:05Z: PR #438 extended again (head 88add881): eight texts (T128 a07, python-pin a01/a02 and P1-15 a03 added); CI rerunning; approval pending.
- 2026-10-20T07:31:17Z: #438 merged as main f7ed0142 (D-024-38); `gh pr update-branch 436` next, then CI, sweep (GitGuardian refuted), audit, gate, merge.
- 2026-10-20T08:31Z: records PR #443 merged at 08:21:55Z moved main to 1f97c525, so `gh pr update-branch 436` -> head 3dbb6542 (C-110); CI reruns; the chain follows in the serial queue (#441 first, started 2026-10-20T08:31Z).
- 2026-10-20T11:45Z-12:06Z: chain on the re-based head a561e640 (CI green except GitGuardian, refuted; sweep 0 gaps; local review 0 findings): task-level audit `…-audit-a561e64.md` `Verdict: incorrect`, 3 P2 + 2 P3: [P2] trusted_exec_contract.py:126 output-read escape detection checks access time only for `self.input`; [P2] :131 an adjacent temporary file written before refusing the output passes; [P2] orchestration record:74 the revise-1 change of `passwd_home()` from mandatory dscl/getent to an optional cross-check had no hashed amendment while task line 136 kept the requirement (RESULT `amendments=0`); [P3] validation.md:129 commands keep undefined `$UT`, `$PY`, `$PY310`, `$H`; [P3] pr-feedback.json:70 the GitGuardian issue comment is dispositioned `no finding` instead of the refutation. Dispositions: the two implementation P2 are advisory rows owned by the follow-up (rounds spent: round 1 + revise 1); the orchestration P2 is fixed by amendment 1 (line 136 rewritten to the measured behaviour, `previous_sha256 dd754911…` -> `f9f09083…`, dispatched to a011 as a records-only round with the task-copy update); the P3 evidence by the same records commit (literal commands); the P3 sweep disposition by the `issuecomment-6281175171` row in `436-extra.tsv`. The amended text reaches main through the next records PR (D-024-40); the regime check is re-run after that merge.
re-plan: evidence (rows audit:9545e59:2, audit:9545e59:3, audit:9545e59:4; the class reached three rows across the a01 audits: validation records that cannot be replayed or that over-claim) — specification: every recorded command in report.md and validation.md is the literal command that ran, with its exit code and output, and every claim about a run names its log; no shell variable, placeholder or summary stands in for a command; design: the worker writes commands from a command log (the a06 lineage's `*-commands.json` plus `measure.md` pattern) rather than by hand, and the orchestrator's evidence check refuses a validation whose recorded commands contain unexpanded `$VAR` tokens or whose base/candidate counts disagree with their claims (`result-evidence-check.sh`, orchestrator-side); implementation: the records-only commit of amendment 1 replaces the placeholders in this lineage; the check is an item of `dotfiles-T133-result-precheck-followup-a01` (D-024-46); verification: the task-level audit of the final head reports no evidence-class finding, and the evidence check passes on that head.

audit:a561e64:1	escape-detection-gap
audit-finding: a561e64:1 not-applicable:advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (output-read escape detection checks access time only for self.input, trusted_exec_contract.py:126); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md
audit:a561e64:2	escape-detection-gap
audit-finding: a561e64:2 not-applicable:advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (an adjacent temporary file written before refusing the output passes, :131); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md
audit:a561e64:3	unhashed-text-change
audit-finding: a561e64:3 fixed-by-amendment-1 (the TASK line of 2026-10-20T12:2xZ, previous_task_sha256 dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c -> f9f09083a9b314fb0417e0529541ea539f3c2f500cfc5f25a40c564d11a48258; the records-only commit of a011 updates the copy; the commit sha is written here at its RESULT)
audit:a561e64:4	evidence-placeholders
audit-finding: a561e64:4 fixed-by-the-records-commit-of-amendment-1 (literal commands replace $UT/$PY/$PY310/$H; sha at the RESULT)
audit:a561e64:5	disposition-label
audit-finding: a561e64:5 fixed-in-the-next-sweep (436-extra.tsv row issuecomment-6281175171: the refutation of the five synthetic-fixture findings); evidence=grep -c issuecomment-6281175171 .agents/worklog/orchestrator-glue/436-extra.tsv
- 2026-10-20T14:26Z: INV-6 S2 (revises 2): reset `dotfiles-T133-trusted-exec-contract-tests-a02` (records-only, code unchanged at 612f75f5) anchored by a009's review (0b1923a6…), reset record written; the a02 TASK dispatched to a011; PR #436 continues under a02.
