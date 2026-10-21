---
{
  "audit_findings": [
    {
      "evidence": "git show 7fad8353:tests/unit/test_regime_ci.py | grep -n 'def test_': test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (cases 'precheck head', 'precheck side', 'precheck late', 'precheck sha', 'caps outside', 'caps tests', 'caps worded') and test_regime_ci_passes_a_records_only_pr_with_no_target; the threat row names only test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier",
      "n": "1",
      "reason": "not-applicable: the invalid-precheck, exceeded-cap and no-target controls are each tested at 7fad835 by two other named tests; the threat row names one selector of three, a text defect owned by dotfiles-T133-regime-ci-followup-a01 (threat-row-selector)"
    },
    {
      "evidence": "git diff --stat b5af2030 a5a9f4e1 = .orchestration/dotfiles-T133-regime-ci-a02/validation.md only (50+/18-); git diff --name-only a5a9f4e1 7fad8353 = main's #416 files only (7fad8353 = Merge branch 'main' into tools/regime-ci-a01); regime-ci.py line 125 states the same rule for precheck.json",
      "n": "2",
      "reason": "not-applicable: the bootstrap run on the code head b5af2030 is the run on 7fad8353 for every executed file, since the two differ only by the evidence file and the merge of main; the text requirement (the final-head command) is circular, as regime-ci.py itself states for precheck.json, and its rewording is owned by dotfiles-T133-regime-ci-followup-a01 (evidence-head-mismatch, 2 of 3)"
    },
    {
      "evidence": "grep -n 'Owned by dotfiles-T133-regime-ci-followup-a01' .orchestration/acceptance/dotfiles-T133-regime-ci-a02.md",
      "n": "3",
      "reason": "not-applicable: the record defect is corrected in this record (the Owned by section now carries the stale-pr-description row and the two rows above); a record edit is the orchestrator's, not a worker round"
    }
  ],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-regime-ci-a02 round=1 reset_of=dotfiles-T133-regime-ci-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T133-regime-ci-a02.md task_sha256=015a5e0f48f07cc12a2e7b65241de3f1e8547d89e091591fe1a7bbd7daf0aa90 deadline=none done_signal=AGMSG-RESULT note=a008:S1-redesign-of-a01(trust-boundary-pr-input)"
  ],
  "format": 1,
  "head": "7fad8353b04c7587a009f4349b9db215c2333120",
  "ledger": [
    {
      "class": "trust-boundary-pr-input",
      "id": "4308651010"
    },
    {
      "class": "trust-boundary-pr-input",
      "id": "4308651011"
    },
    {
      "class": "trust-boundary-pr-input",
      "id": "4308651013"
    },
    {
      "class": "trust-boundary-pr-input",
      "id": "audit:f7d2c48:1"
    },
    {
      "class": "evidence-head-mismatch",
      "id": "audit:f7d2c48:2"
    },
    {
      "class": "stale-pr-description",
      "id": "audit:f7d2c48:3"
    },
    {
      "class": "threat-row-selector",
      "id": "audit:7fad835:1"
    },
    {
      "class": "evidence-head-mismatch",
      "id": "audit:7fad835:2"
    },
    {
      "class": "records-form",
      "id": "audit:7fad835:3"
    }
  ],
  "pr": 418,
  "replans": {
    "trust-boundary-pr-input": {
      "design": "pull_request_target with permissions contents: read, checkout of the base sha, git fetch of refs/pull/<n>/head as a detached ref, regime-ci.py --base <base> --head <head> reading the head through git show, the checker on a temporary copy; the first PR proves its own job by a local run of the same command line",
      "implementation": "the a02 reset (review profile) keeps the a01 worker's fixes and amendment 1 and adds the three Bot P1 fixes with one item each",
      "specification": "the job never executes code from the pull request head: the workflow, regime-ci.py and the checker run from the base commit, the head is fetched as data and read only through git show; every PR-controlled input (task copy, result.txt, precheck.json, branch name) is a claim; the copy is verified against the dispatched text at the base, unverifiable is a warning until REGIME_REQUIRE_DISPATCHED=1 (a decision row at promotion) and a failure after; the records-only exemption is decided from the head's changed paths alone, never from the branch name",
      "verification": "a workflow-shape test (trigger, permissions, base checkout, pull-ref fetch, no head execution), a head that modifies the verifier does not change the verdict, content-based exemption, and the unverifiable warning-or-failure under the flag"
    }
  },
  "searches": [
    {
      "class": "trust-boundary-pr-input",
      "records": []
    }
  ],
  "task": "dotfiles-T133-regime-ci-a02"
}
---

# Acceptance record: dotfiles-T133-regime-ci-a02

Plan 024 P1-11, the S1 redesign of `dotfiles-T133-regime-ci-a01` (class trust-boundary-pr-input: the Bot's three P1 on 4a921414; the class table and the `re-plan:` are in the a01 record; M-20261018-14, C-75). Redesigned by a review-profile context (`.agents/worklog/orchestrator-glue/redesign/p111-a02.md`, prompt `p111-a02-redesign-prompt.md`); seat a008 (worker-f, Claude) continues PR #418 from 4a921414. The job runs from the base commit under `pull_request_target` with `contents: read`, reads the head as data, verifies the copy against the dispatched text at the base (unverifiable is a warning until `REGIME_REQUIRE_DISPATCHED=1`), and decides the records-only exemption from the changed paths alone. Owner of advisory P2: `dotfiles-T133-regime-ci-followup-a01` (written when the first appears).

- 2026-10-18T21:0xZ: task text installed, `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a008 (the line above; the full note is in the bus history).
- 2026-10-18T21:37:56Z: a008's worker review of 4a921414..bcbd6949 found a P0 (trust-boundary-pr-input, the lineage's 4th row): item 2 fed the head's task copy to the base checker, whose C10 runs `git grep -qF <literal>` unquoted (`--open-files-in-pager=CMD` ran a marker in the pull_request_target job), plus a P2 (C6 reads a design path outside the checkout); a008 proposed the re-plan within allowed_files and asked for an objection before its RESULT.
- counters before the send (`scripts/regime-counters.sh dotfiles-T133-regime-ci-a02 --history-only`, 21:4xZ): task=dotfiles-T133-regime-ci-a02 tasks=1 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-18T21:00:17Z..non
- 2026-10-18T21:4xZ: amendment 1 (the sentence withdrawn; the checker reads only base-dispatched bytes; unverifiable copies skip it with a warning; authenticated supersession; --no-renames; the checker hardening to P1-12 a02) dispatched to a008, task sha256 807c6b7446b7bbf795aa2b6aa6db1c46b9543b8ac953e40b4309dfd735322219 (previous 015a5e0f…). INV-6 after this send: amendments 1. The P0 is the orchestrator's prompt again (the redesign prompt said "the checker invoked on a temporary copy of the task file" without saying whose bytes): M-20261018-14's class, logged under it.
- 2026-10-18T22:29:16Z: RESULT round 1 from a008: PR #418 head f7d2c48dad9fcf37b7111003b609e80d320f666a (code head 1ee15af1) on 3e41e36a, branch `tools/regime-ci-a01` continued from 4a921414; `task_copy=807c6b74…` (amendment 1's sha); changed: regime.yml, regime-ci.py, test_regime_ci.py, test_workflow_security.py (+1 line), the a02 evidence, the a01 copy deleted; CI 10 pass (no regime run: premise 6, the base has no regime.yml); the three Bot P1 `fixed:bcbd6949` (4308651011 also 1ee15af1); six red-then-green tests plus the two of amendment 1, 27 mutants killed; the worker review's round 1 found the P0 (the base checker fed a PR's text) that became amendment 1, round 2 correct; the bootstrap local run in an isolated base checkout: exit 0 with the expected warnings; caps 324/330 outside, 405/480 tests; residual: the checker hardening (P1-12 a02) should land before this merges (no current exposure: 514 dispatched texts scanned), and a task directory touch borrows an old task's policy; `bot=none` for the a02 head. `status=pending-integration` sent 22:3xZ; the chain is queued after #412.

4308651010	trust-boundary-pr-input
4308651011	trust-boundary-pr-input
4308651013	trust-boundary-pr-input

## Audit of f7d2c48 (2026-10-18T22:57Z): two P2, one P3; revise 1

- The chain (local review 0 findings; the sweep 0 gaps; the three Bot-thread ledger rows added by hand after the record-step gap) ran the audit: `Verdict: incorrect` (`.orchestration/validation/dotfiles-T133-regime-ci-a02-audit-f7d2c48.md`): (1) P2 implementation `regime-ci.py:260`: supersession checks only that base-dispatched texts exist, not that both head copies are byte-equal to them (an altered predecessor copy still passed); (2) P2 evidence `validation.md:221`: the bootstrap local run targets the code head 1ee15af1, not the final head f7d2c48d (six evidence files more), although the text requires the final-head command and output; (3) P3 orchestration: PR #418's description still describes the withdrawn a01 design.
- decision: (1) and (2) get revise 1 (a02's one round; INV-6 amendments 1, revises 0 → 1): the byte-equality check with its red-then-green test, and the bootstrap run redone on the final head and pasted; (3) is not evidence (the record is) and `gh pr edit` is a live ask rule for every seat, so it is a records-form row for the owner task (`stale-pr-description`, as PR #408's), not a round item. The security-profile review runs on the revise-1 head before the gate.

audit:f7d2c48:1	trust-boundary-pr-input
audit:f7d2c48:2	evidence-head-mismatch
audit:f7d2c48:3	stale-pr-description

- counters before the send (`scripts/regime-counters.sh dotfiles-T133-regime-ci-a02 --pr 418`, 22:58Z): `tasks=2 amendments=1 questions=0 results=1 withdrawn=0 revises=0 first_result_head=f7d2c48d bot_p1_heads_after_result=0`; `S1: class=trust-boundary-pr-input count=3 re-plan=missing source=record` until the a01 record's `replans` object was copied into this record's block (22:59Z); `searches` for the class set (no mistake record carries the slug).
- 2026-10-18T23:0xZ: `status=revise previous_head=f7d2c48…` sent to a008 (wJ:p3), to run before its F1 owner task: byte-equality of both copies before supersession with its test; the bootstrap run redone on the final head; the stale PR description as an owner row. INV-6 after the round: amendments 1, revises 1 (no further round).
- 2026-10-18T23:50:03Z: revise-1 RESULT from a008: PR #418 head a5a9f4e17879055f1d48ae2daf29009dc1d7af36 (code head 3d695ed1, previous f7d2c48d); `task_copy=807c6b74…` (amendment 1's sha); items: a reset_of predecessor is superseded only when both head copies are byte-equal to their base-dispatched texts (an altered predecessor copy is a violation; `check=` test red at 9ee208d5, green at 3d695ed1); the bootstrap local run pasted on b5af2030 and rerun on the final head (identical output); the stale PR description left as the owner row; the receipt's reviewer field is one word; 28/28 mutants killed; CI 10 pass; `bot=none` on the revise push; caps 325/330 and 417/480; INV-6 amendments 1, revises 1 (no further round). `status=pending-integration` sent 23:5xZ; the chain is queued after #411 and #420; the security-profile review runs on a5a9f4e1 at once.
- 2026-10-18T23:5xZ: the security-profile review of a5a9f4e1 (`.orchestration/validation/dotfiles-T133-regime-ci-a02-security-a5a9f4e.md`): `Verdict: correct` (the merge glue's security guard is satisfied for this head).

## Audit of 7fad835 (2026-10-19T01:02Z): two P2, one P3; no worker round

- The chain re-ran after the lineage audit rows were added by hand (the record step drops `audit:<sha7>:n` rows; the P1-6 item): sweep 9 items, 0 gaps; local review 0; the audit of the update-branch head 7fad8353 (`.orchestration/validation/dotfiles-T133-regime-ci-a02-audit-7fad835.md`): `Verdict: incorrect`: (1) P2 specification `task.md:18`: the `closed` threat row's one selector does not test invalid prechecks, exceeded caps or the no-target exemption; (2) P2 evidence `validation.md:246`: the bootstrap output targets the code head b5af2030, not 7fad8353; (3) P3 orchestration `record:71`: the stale-description finding was declared an owner row without an `Owned by` entry. The auditor's INV-6 line: one pre-RESULT fix and one revise reach C-61's two-round cap.
- counters (`scripts/regime-counters.sh dotfiles-T133-regime-ci-a02 --pr 418`, 01:03Z): `tasks=2 amendments=1 questions=0 results=2 withdrawn=0 revises=1 first_result_head=f7d2c48d bot_p1_heads_after_result=0`; `S1: class=trust-boundary-pr-input count=4 re-plan=present source=record`.
- decision: no worker round (the C-61 cap is reached, and none is needed): (1) is covered at 7fad835 by `test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr` (precheck head/side/late/sha, caps outside/tests/worded) and `test_regime_ci_passes_a_records_only_pr_with_no_target`; the threat row names one selector of three, an owner row (`threat-row-selector`); (2) `git diff --stat b5af2030 a5a9f4e1` is validation.md alone and a5a9f4e1→7fad8353 is the merge of main, so the code-head bootstrap is the final-head bootstrap for every executed file; the "final-head command" wording is circular (regime-ci.py line 125 states the same for precheck.json) and its rewording is an owner row (`evidence-head-mismatch`, the class's second row); (3) corrected below in this record (`records-form`). The security-profile review of 7fad8353 runs before the gate (the glue's guard names the merged head).

audit:7fad835:1	threat-row-selector
audit:7fad835:2	evidence-head-mismatch
audit:7fad835:3	records-form

## Owned by dotfiles-T133-regime-ci-followup-a01

- `audit:f7d2c48:3` stale-pr-description: PR #418's title and description still describe the withdrawn a01 design (`pull_request`, head execution); the owner edits them (`gh pr edit` is a live ask for every seat; the operator answers once).
- `audit:7fad835:1` threat-row-selector: the `closed` disposition of the regime-ci.py threat row names all three tests that close it (the base-verifier test, the violation table, the no-target exemption test).
- `audit:7fad835:2` evidence-head-mismatch: the Check clause's "bootstrap on the final head" is reworded as "on the code head, with the evidence commit touching only `.orchestration/<task>/`", the rule regime-ci.py already applies to precheck.json; the validation record states both identities.
- 2026-10-19T01:05:07Z: the security-profile review of the audited head 7fad8353 (`.orchestration/validation/dotfiles-T133-regime-ci-a02-security-7fad835.md`): `Verdict: correct`, no findings; the glue guard is satisfied for the merged head. Gate and merge follow (`integrate-merge.sh dotfiles-T133-regime-ci-a02 7fad8353… 418`).
- 2026-10-19T01:10:30Z: gate passed (`integrate-merge.sh`, the glue security guard satisfied by the 7fad835 review); `gh pr merge --squash --match-head-commit 7fad8353…` → main 0e496ce7 (`feat(orchestrator): the regime CI job checks a PR against its task copy (T133 regime-ci a01, plan 024 P1-11) (#418)`); local main fast-forwarded; `status=accepted` sent to a008 with the rebase note for its #410 branch. Owner rows above pass to `dotfiles-T133-regime-ci-followup-a01` (dispatched after a seat frees).
- `ci:39185982423:1` stale-base-sha (found 2026-10-19T01:34Z on PR #420 head 0e5d8807, reported by a010 01:39:34Z, verified by the orchestrator with `gh run view 39185982423` and `gh api pulls/420`): regime.yml checks out and passes `github.event.pull_request.base.sha`, which GitHub updates only when the PR synchronizes, so a PR whose recorded base predates regime-ci.py (740772ef < 0e496ce7) fails with a missing verifier; the job resolves the base branch tip at run time (`refs/heads/${{ github.base_ref }}`, the protected branch, which the PR cannot alter) for both the checkout and `--base`, and regime-ci.py accepts a base that is a descendant of the merge base; one red-then-green workflow-shape test in tests/unit/test_workflow_security.py and one regime-ci test.
- correction (2026-10-19T02:4xZ, from a011's RESULT note): the row `ci:39185982423:1` above says base.sha "updates only when the PR synchronizes"; the run shows base.sha was the fork point of the head (740772ef) at the event, so the precise statement is "pull_request.base.sha is the base at the PR's fork point as recorded for the event, not the base branch tip"; the fix (the base branch tip at run time) is unchanged.
