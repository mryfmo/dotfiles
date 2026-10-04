# AGMSG-TASK dotfiles-T68-gate-audit-evidence-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 2, dotfiles-T68). Depends on T67 (merged as 57885db1: the `<id>-audit-<sha7>.md` naming contract). Queued for the next free worker; its files (`scripts/require-crit-review.py`, its test, `rules/pr-integration.md`) are disjoint from every in-flight task.

## Objective

Principle 10 / §2b-6: acceptance without a task-level audit of the final head is stopped mechanically by the integration gate.

1. `scripts/require-crit-review.py`: add env constants `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS` (same style as `REVIEW_EVIDENCE`/`PR_FEEDBACK_EVIDENCE`, lines ~17-21) and a new `audit_errors(root, head)` called from `main` (~576-640) after `pr_feedback_errors`, required only when `args.base` is set **and** `review_reasons` is non-empty (so `.orchestration`-only boundary PRs need no audit).
2. Checks: the path must lie under `.orchestration/validation/` (reuse `feedback_path_error`'s rule); the file name must match `^(?P<task>.+)-audit-(?P<sha>[0-9a-f]{7,40})\.md$` and `head.startswith(sha)`; the verdict source is `<path>.last.md` if it exists, else `<path>`; the verdict is the last non-blank line and must match herdr-agents' regex (`^\s*Verdict: (correct|incorrect|blocked)\s*$`). `correct` → pass. `incorrect` → `AUDIT_DISPOSITIONS` must name a file under `.orchestration/acceptance/` containing one line `audit-finding: … not-applicable:<reason ≥ 20 chars>` per finding, findings counted as lines matching `^\s*\[P[0-3]\]` in the verdict source (reuse `PR_FEEDBACK_DISPOSITION`/`FAILURE_REASON_MIN_CHARS`); only `not-applicable` is accepted, because a `fixed:` moves the head and needs a fresh audit (say so in the error text). `blocked` or missing → fail.
3. `tests/unit/test_require_crit_review.py`: cases for missing env, wrong sha, `.last.md` precedence, `incorrect` with and without dispositions, `blocked`, and the boundary-PR exemption.
4. `home/dot_config/claude/rules/pr-integration.md`: one bullet naming `AUDIT_EVIDENCE` (and `AUDIT_DISPOSITIONS` for `incorrect`) in the gate command.

Forbidden: changes to the review-evidence or PR-feedback logic; new CLI flags; herdr-agents; SKILL/other rules (T69).

[memory:decision] dotfiles-T68 (operator 2026-10-03): `make require-crit-review` with BASE requires `AUDIT_EVIDENCE=<.orchestration/validation/<id>-audit-<sha7>.md>` whose sha matches HEAD and whose last `Verdict:` is `correct`, or `incorrect` with every finding dispositioned `not-applicable` in the acceptance record (`AUDIT_DISPOSITIONS`); `.orchestration`-only PRs are exempt.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/gate-audit-evidence origin/main` (57885db1 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `scripts/require-crit-review.py`, `tests/unit/test_require_crit_review.py`, `home/dot_config/claude/rules/pr-integration.md`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T68-gate-audit-evidence-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
uv run python -m unittest tests.unit.test_require_crit_review 2>&1 | tail -3
make unit-test
make validate-agent-assets
mise x node npm:prettier -- prettier --check home/dot_config/claude/rules/pr-integration.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review of that head; fix P0/P1 inline findings and repeat; close your crit server if Plan Mode opened one; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## Dispatch

- 2026-10-04 02:52Z to `claude-standard-dot-a006` (worker-d, wY:p2) right after its T88 RESULT, per the parallel-execution rule (freed worker re-tasked at once). T88 acceptance is still pending: keep `docs/parallel-execution-rule` in worker-d untouched and branch from `origin/main` (138e6a72 or later). Disjoint from T91 (`validate-agent-assets.py`, a005) and T65 (`agent-stop-gate.sh`, a007).

## PONG decision 1 (orchestrator, 2026-10-04 03:50Z) — Codex AGENTS.md mirror

`home/dot_config/codex/AGENTS.md` "PR 統合" is the Japanese mirror of `rules/pr-integration.md`; its fourth bullet names the gate command, so leaving it without `AUDIT_EVIDENCE` would contradict the new rule bullet. Allowed file added: `home/dot_config/codex/AGENTS.md`, that one bullet only, saying the same thing as the pr-integration bullet (`AUDIT_EVIDENCE=<.orchestration/validation/<id>-audit-<sha7>.md>` required when `BASE` is set and the diff needs review; `AUDIT_DISPOSITIONS=<acceptance record>` for an `incorrect` verdict; `.orchestration`-only PRs exempt). Disposition for 4175944624: `fixed:<that commit>`. The P1 4175944623 and P2s 4175944626/4175944628 are in scope as you said; fix all four in one commit, then `gh pr update-branch` if `main` moved, CI, Bot, RESULT listing every thread.

## PONG decision 2 (orchestrator, 2026-10-04 04:30Z)

- 4175981351 (audit evidence not bound to the feedback task): `fixed:22efc32c`, pending its audit.
- 4175981346 (root `AGENTS.md:51`, the agmsg-orchestration SKILL, the gh-first-workflow skill and the Makefile comment still show the gate without `AUDIT_EVIDENCE`): `not-applicable` for this PR. T68 is the gate code plus its own rule bullet; every other gate mention is rewritten by T69 (protocol and docs unification), which is dispatched right after T68 merges and lists exactly those files. The SKILL is also in flight on this worker's T88 branch, so editing it here would conflict with that PR. The orchestrator replies on the thread; the T69 task file names the four locations.

## Revise round 1 (orchestrator, 2026-10-04 06:40Z) — task-level audit of 3ba270d6 is `incorrect`

Findings (`.orchestration/validation/dotfiles-T68-gate-audit-evidence-a01-audit-3ba270d.md.last.md`) and what to do:

1. **P1, `.last.md` symlink to another task's audit.** The companion is checked for location only; a `<audit>.md.last.md` that resolves to another task's older `correct` audit passes. Fix: apply the same name check to the resolved companion (strip `.last.md`, then `AUDIT_NAME` with the same `<task>` and a sha prefix of HEAD), and refuse a companion whose resolved name differs from `<audit>.md.last.md`.
2. **P1, transcript fallback accepts quoted text; P2, empty `.last.md` falls back.** Resolve both by requiring the companion: `AUDIT_EVIDENCE` passes only when `<audit>.md.last.md` exists with non-blank content and its last non-blank line is the verdict; a missing or empty companion is a missing verdict ("re-run the audit; codex wrote no final message"). Delete `final_codex_block` and its tests. herdr-agents may keep its own display fallback; the gate does not have to mirror it. Update the pr-integration bullet and the Codex AGENTS.md mirror ("from `<file>.last.md`, which must exist with content").
3. **P3, evidence.** The validation file records the CompactionDB command with a `<the text above>` placeholder; paste the command as actually run, with the verbatim `--content`, and its UUID.

Allowed files: as before plus the two rule mirrors already in scope. One commit; `gh pr update-branch 246` if `main` moved; CI; Bot (paginated listing); RESULT naming every thread. Do this before the T88 round 2 that follows.

## Revise round 2 (orchestrator, 2026-10-04 08:20Z) — evidence corrections only, no code change

The task-level audit of 5168613a (`…-audit-5168613.md.last.md`) found no implementation defect and two evidence gaps:

1. `.orchestration/learning/dotfiles-T68-gate-audit-evidence-a01.md:3` still says an empty `.last.md` falls back to the transcript; the final head rejects a missing or empty companion. Update the learning note.
2. The report claims three task revisions verified (`3959867c…`, `fcbe596a…`, `7d991601…`, plus the round-1 rev) but the validation file holds no `sha256sum` outputs for them. Paste the verification commands and outputs (re-run `sha256sum` on the current task file for this round, and cite the earlier revs from your session log if they are no longer reproducible, saying so).

No commit, no push: the head stays 5168613a. Reply with `AGMSG-PONG v1 task_id=dotfiles-T68 status=alive note=artifacts-corrected` when done; the orchestrator re-runs the task-level audit on the same head.
