# AGMSG-ACCEPTANCE dot-herdr-worker-relaunch-T25-a01

Round 1 RESULT 2026-09-27T00:26:23Z status=blocked: all deliverables implemented on 3be4656 (PR #186); CI test jobs failed on a pre-existing main breakage — the orchestrator's 20f3e9e ccusage bump left 20.0.22 pins in test.yaml/test_statusline_tools.py/check-statusline-tools.py, so main's own Unit test run at 20f3e9e was red (the orchestrator had only checked the later .orchestration-only pushes, which skip test jobs — orchestrator process error, recorded).

Orchestrator remediation: ccusage pin sync landed on main as 668ff64 (machine-lifecycle exemption, make-upgrade pin follow-through); main CI green including Unit test.

Round 2 RESULT 2026-09-27 ~01:0xZ status=ready_for_review: branch rebased onto 668ff64, one authorized pinned force-with-lease (recorded verbatim in validation), final head f9b158a.

## Adversarial review (orchestrator, from origin refs)

- Round-1 diff fully reviewed: `find_managed_workspaces`/`single_managed_workspace` (pane-evidence lookup fixing the real root cause — attach-mode workspaces keep their own label, so the old `find_existing_workspace` full-mode-label match missed them and full mode spawned a duplicate); `--restart-worker` (in-place restart, never creates panes/workspaces, exit-2 cases mirror attach refusals); full-mode agentless-labeled-pane heal; `has_claude_pane` worker exclusion and attach self-guard (claude worker's SessionStart --attach no longer relabels its pane); README paragraph; agmsg-orchestration rule bullet; validator `--restart-worker` README token check; tests — 7 new cases that fail on origin/main code (mutation check pasted in validation), 447 unit tests OK.
- `single_managed_workspace` exit 2 inside `$( )` propagates via `set -e` on the assignment — verified.
- Round-2 head verified byte-identical to the reviewed patch: `diff <(git diff 8b0f68f..3be4656) <(git diff 668ff64..f9b158a)` empty.
- CI fully green on f9b158a; the previously skipped shfmt/ShellCheck/python-unit/bats steps ran and passed on all runners.
- Worker exceeded the report contract by re-deriving the root cause with read-only live queries; no correctness, regression, security, or omission findings.

## Review guard

make require-crit-review satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-herdr-worker-relaunch-T25-a01-receipt.md (resolved review-scope approval record r_e54361, crit session 310deb97d86f, exported JSON at .orchestration/validation/dot-herdr-worker-relaunch-T25-a01-crit.json).

**Decision: ACCEPTED.** Merge #186 --squash (no --delete-branch while worker-c holds the branch); deployment orchestrator-side (chezmoi apply both clones), live E2E of `--restart-worker` on the wF pair as part of deployment; T26 (worker --advisor fable) dispatches after this lands.

[memory:decision] T25 accepted 2026-09-27: herdr-agents enforces one-workspace-per-pair (pane-evidence managed-workspace lookup, full-mode duplicate guard, agentless-pane heal) and gains --restart-worker; codified in README + agmsg-orchestration rule + validator check + unit tests. PR #186 squash-merged.

cost: n/a (worker report gives no token figures)
