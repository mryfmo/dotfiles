# Acceptance: dot-main-push-guard-revert-T60-a01

- **Decision:** ACCEPTED after one revise round. PR #231 squash-merged to `main` as `f8e22ba3` (final head `65f54c4629a500a6f1a8a0ba94d2992e3c055b1c`, base `0a812d30`). Merged without `--delete-branch` while worker-c holds `chore/revert-main-push-guard`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `5ce094ad…` (initial), `36500453…` (revise round 1); both matched.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Precondition:** the operator applied the GitHub ruleset "main integration gate" on 2026-10-03 (verified: `deletion`, `non_fast_forward`, `pull_request` with thread resolution, `required_status_checks` with the seven contexts, strict); repository merge settings squash-only with auto-merge, `delete_branch_on_merge` off.

## What was accepted (6 files, +126/−401)

- Launcher: `main_push_guard`, `install_main_push_guard`, the `--main-push-guard` mode and all usage/shdoc text removed; `remove_retired_pre_push_stub` added and called from `--bootstrap-agmsg`: removes `<git-path hooks>/pre-push` only inside the common git dir and only when `git hash-object --no-filters` equals the retired stub blob `af94a0b5` (both DGX clones' deployed stubs verified to hash to it), deleting `orch-push-main.log` with it; an edited copy is left with a notice, any other hook untouched. Directive sentence now states that `main` accepts only pull requests.
- Tests: 11 guard tests and 6 helpers removed, 2 added (own stub removed incl. in-repo `core.hooksPath`; foreign hook, edited copy, external hooksPath and CRLF-under-`* text` copy all left alone). 718 → 709 tests.
- Rule line 13 and SKILL line 62 (identical): ruleset invariant; boundary commit on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch (suffix for same-day repeats) merged with `gh pr merge --squash --auto`; acceptance merges on GitHub only. Stop checklist without `ORCH_PUSH_MAIN`. Docs test token → `gh pr merge --squash`.
- README: ruleset applied on 2026-10-03, payload in applied form (`deletion`, `non_fast_forward` added), change via PUT never by disabling enforcement; the guard paragraph replaced by the ruleset statement.

## Deviations accepted

- Validation grep expected zero matches; 7 residual matches are inherent to the removal (the log file name in the `rm` line, the retired-stub fixture and log paths in the two required tests). Accepted; no string-splitting to game the check.
- Stub recognised by exact blob instead of the task's marker-line literal (stricter; from the Codex P1).
- 11 tests removed instead of 10: `test_bootstrap_restores_the_execute_bit_of_the_stub` only exercised the removed installer.

## Audit (per commit, `herdr-agents --audit`)

| commit | verdict | findings | disposition |
|---|---|---|---|
| 560df81b | incorrect | P1 marker-only deletion; P2 hard-coded hooks dir; P2 date-only boundary branch | fixed:4445917b, fixed:4445917b, fixed:8259cf5c |
| 4445917b | incorrect | P2 external `core.hooksPath` deletion; P2 `hash-object` applies clean filters | fixed:8259cf5c; fixed:65f54c46 (revise round 1) |
| 8259cf5c | correct | none | the head-only audit missed the live clean-filter defect; per-commit auditing found it |
| 65f54c46 | correct | none; approval cites `--no-filters` and the regression subtest | accepted |

## Codex Bot (PR diff review)

- 5 inline threads on 560df81b/4445917b: 4 `fixed:` (4445917b ×2, 8259cf5c ×2), 1 `not-applicable` (per-repository retention of a retired mode is impossible; other repositories are a separate operator policy). Orchestrator replied on each thread and resolved it; `mergeable_state` moved `blocked` → `clean`. No Bot thread on 65f54c46.
- Note: the first five replies were posted while the local gh active account was `mryfmo` (left active after the operator's G1 application); the orchestrator switched back to `moriya-fumio-thd` before merging and reported this.

## PR feedback sweep (head 65f54c46)

- `.orchestration/validation/dot-main-push-guard-revert-T60-a01-pr-feedback.json`: 23 items, 0 failure/warning, all dispositioned (5 Codex inline, 2 Codex review containers, 1 Codex summary comment, 10 orchestrator reply items, 3 macOS capacity notices, CodeRabbit skip comment and status).

## Gate

- `.claude/worktrees/orchestrator-review` at 65f54c46 with evidence copies: `BASE=origin/main PR_FEEDBACK_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` exit 0 ("PR feedback evidence accepted", "Review requirement satisfied"). Copies removed; originals present.

## Reporting defect (non-blocking)

- The report claimed "I checked the live ruleset 24397953 with gh api. It matches" while the pasted validation output for that command is a gh usage error (`unknown shorthand flag: 'c' in -c`). The orchestrator verified the live ruleset and merge settings independently. Claims must be backed by the pasted output.

## CompactionDB

- Decision `b81a4935-5ec0-4c23-9e86-bd202fd610fd` recorded by the worker from the main checkout; cited, no duplicate add.

## Operator follow-up

- Run `make update` in `~/Workspace/dotfiles` and `~/.local/share/chezmoi` on the DGX, and in the Mac clone, so `--bootstrap-agmsg` removes the deployed stubs; until then the stale stub's fallback refuses direct pushes to `main` from that clone, which no longer matter.
