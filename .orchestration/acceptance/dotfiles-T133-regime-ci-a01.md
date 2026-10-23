---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-regime-ci-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T133-regime-ci-a01.md task_sha256=da3965e6b10fd3fe743f2aee8849ee67b1cc1d55924357407485f7ca41610fbf deadline=none done_signal=AGMSG-RESULT note=a008:plan-024-P1-11(programs-item-6):regime.yml-and-regime-ci.py"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "replans": {
    "trust-boundary-pr-input": {
      "design": "pull_request_target with permissions contents: read, checkout of the base sha, git fetch of refs/pull/<n>/head as a detached ref, regime-ci.py --base <base> --head <head> reading the head through git show, the checker on a temporary copy; the first PR proves its own job by a local run of the same command line",
      "implementation": "the a02 reset (review profile) keeps the a01 worker's fixes and amendment 1 and adds the three Bot P1 fixes with one item each",
      "specification": "the job never executes code from the pull request head: the workflow, regime-ci.py and the checker run from the base commit, the head is fetched as data and read only through git show; every PR-controlled input (task copy, result.txt, precheck.json, branch name) is a claim; the copy is verified against the dispatched text at the base, unverifiable is a warning until REGIME_REQUIRE_DISPATCHED=1 (a decision row at promotion) and a failure after; the records-only exemption is decided from the head's changed paths alone, never from the branch name",
      "verification": "a workflow-shape test (trigger, permissions, base checkout, pull-ref fetch, no head execution), a head that modifies the verifier does not change the verdict, content-based exemption, and the unverifiable warning-or-failure under the flag"
    }
  },
  "searches": [],
  "task": "dotfiles-T133-regime-ci-a01"
}
---

# Acceptance record: dotfiles-T133-regime-ci-a01

Plan 024 P1-11 (programs item (6)): the `regime` GitHub job and `scripts/orchestrator/regime-ci.py` (task copy, precheck binding when present, allowed files, caps, the tracked checker as a subprocess; one violation per line; records-only PRs pass with a no-target line). Optional check first; promotion to a required context is the operator's ruleset step after P1-14. Seat: a008 (worker-f, Claude), after its #416 revise-1 RESULT.

- 2026-10-18T13:1xZ: task text written with five pasted premises (new files absent on main; the pinned action shas; the checker's eleven checks; result.txt absent on main; `regime` not among the seven required contexts), `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a008 (the line above; the full note is in the bus history). Disjoint from every in-flight task's files (#409, #410, #411, #412, #415, #416, #417, P1-14).
- 2026-10-18T13:36:50Z: a008 `status=blocked`: PR #418's CI test jobs fail only on `tests/unit/test_workflow_security.py::test_workflows_have_exact_top_level_permissions` (its EXPECTED_PERMISSIONS allowlist names every workflow and lacks regime.yml; by design each new workflow is added there); that file is outside allowed_files. Request: amendment adding `tests/unit/test_workflow_security.py` for one line (`"regime.yml": {"contents": "read"}`) with its threat row. Meanwhile a008 fixes its worker review's P1 (a checker crash passed as clean), P2s (cap sentence with a parenthetical; the precheck ancestor rule strict to `.orchestration/<t>/`; test gaps) and P3s (40-hex precheck head, git failures checked, tab paths, `uv --no-config`); the regime job itself passes on #418; a P2 spec gap: a PR with two task directories (a reset_of lineage) fails each copy, proposed for the follow-up owner. Read at 19:58Z (the orchestrator's session was suspended from about 15:01Z (its last activity: the #416 chain's end at 15:00:51Z; its last bus line at 14:46:16Z) to 19:58Z).
- counters before the send (`scripts/regime-counters.sh dotfiles-T133-regime-ci-a01 --history-only`, 20:03Z): `tasks=1 amendments=0 questions=0 results=0 withdrawn=0 revises=0` (no S line).
- 2026-10-18T20:0xZ: amendment 1 (the one EXPECTED_PERMISSIONS line in tests/unit/test_workflow_security.py with its threat row; regime.yml declares the permissions block; the reset_of two-copies rule: check the latest copy, warn on predecessors) dispatched to a008, task sha256 0bca9954f0cefdc21c289249b9130d41d566c4eaadaf495565874868f04a402d (previous da3965e6…). INV-6 after this send: amendments 1.

## S1 trust-boundary-pr-input (2026-10-18T20:44:53Z), class table, re-plan, withdrawal

- a008's blocked PONG: the Codex Bot review 5564850518 on 4a921414 gives three P1 of one class, all premised on `regime` becoming a required check: 4308651010 the workflow runs regime-ci.py and the checker from the PR head (a PR edits the verifier to pass); 4308651011 the policy binds only to PR-controlled files (dispatched text read from the head, result.txt's hash self-attested); 4308651013 the `orchestration/` exemption trusts `GITHUB_HEAD_REF`. CI 11 pass on 4a921414, the regime job passes on its own PR, amendment 1 done, the worker's review 2 rounds correct; no patch pushed for the three P1 (two contradict the a01 text). a008 proposed A (pull_request with base-sha execution) or B (pull_request_target) and recommended B plus A's base-only dispatched text and same-repo exemption, or merging as optional and owning the three as promotion blockers.

| # | where | finding (class trust-boundary-pr-input) |
| --- | --- | --- |
| 1 | Bot thread 4308651010 on 4a921414 | the workflow executes regime-ci.py and the checker from the PR head |
| 2 | Bot thread 4308651011 on 4a921414 | the copy, allowed_files and caps bind only to PR-controlled files |
| 3 | Bot thread 4308651013 on 4a921414 | the records-only exemption trusts the PR's branch name |

Three rows: S1 (C-59). The root cause is the orchestrator's a01 text (item 1: run regime-ci.py on the PR head; item 2: the dispatched text read at the head; the branch-name exemption), not the worker. Merging as optional and fixing later is refused: the design is known wrong. The artifact goes to redesign.

re-plan: trust-boundary-pr-input -> specification: the job never executes code from the pull request head; the workflow, regime-ci.py and the checker run from the base commit, the head is fetched as data and read only through git show, every PR-controlled input is a claim, the copy is verified against the dispatched text at the base (unverifiable is a warning until REGIME_REQUIRE_DISPATCHED=1 and a failure after), and the records-only exemption is decided from the head's changed paths, never from the branch name; design: pull_request_target with contents: read, checkout of the base sha, the pull ref fetched as data, the checker on a temporary copy, the first PR proven by a local run; implementation: the a02 reset by the review profile keeps the a01 fixes and amendment 1 and adds one item per Bot P1; verification: the workflow-shape test, a verifier-modifying head that does not change the verdict, the content-based exemption, the flag-controlled unverifiable rule.

- 20:4xZ: `AGMSG-ACCEPTANCE … status=withdrawn` sent to a008 (wJ:p3) with the decision (B plus A's parts); a008 holds #418 at 4a921414. The a02 redesign (review profile, prompt `.agents/worklog/orchestrator-glue/p111-a02-redesign-prompt.md`) follows. Mistake M-20261018-14 (the orchestrator's CI-check spec executed PR-head code) and correction C-75.
