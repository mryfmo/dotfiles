# Acceptance: dot-pr-feedback-gate-T38-a01

RESULT received 2026-09-29T09:31Z (revision 1, status=ready_for_review, head
98991e64d99b69b3cc9f869dc7523e8fbe13abb6, PR #210, base origin/main 6fa41a5).
Mid-task PONG 09:12Z asked for a ruling on four review findings; ruling
09:14Z: fix (1) in-PR fail-closed, defer (2)(3)(4) to the security lane.

## Adversarial review (orchestrator, from origin refs only)

- Base: `origin/main` is an ancestor of the PR head; three commits
  (f7433fc carry, fa934f7 optional CodeRabbit + trigger removal, 98991e6
  fail-closed base).
- Carry fidelity: the carry commit touches exactly the 17 files PR #182
  touched (file-list diff empty). For the five auto-merged files the PR's own
  +/- lines are byte-identical between `6026837..origin/pr/182` and
  `origin/main..f7433fc` (Makefile, README, agmsg-orchestration SKILL,
  crit-review.md, codex AGENTS.md; only context lines differ). AGENTS.md:
  main's crit-fallback bullet and the whole `## Audit` section are verbatim;
  the PR bullet is the last bullet of `## Agent Review Evidence`.
- Optional CodeRabbit: `BOT_REVIEWER` and the bot-review-of-HEAD check are
  gone; head-match, base-collector, `fixed:` range, reason-length and
  multiset-coverage checks are untouched (diff read in full). The replaced
  test asserts exit 0 and "PR feedback evidence accepted" with no review item
  collected. Parity token removed; rules say MAY; Convergence bullet dropped;
  README ruleset no longer requires the CodeRabbit context; trigger workflow
  deleted with its parse-step and permissions entries; `.coderabbit.yaml` and
  the pr-integration symlink template remain. Repo-wide grep at the head finds
  no mandatory wording (`.coderabbit.yaml` comment, sample fixture, and the
  "optionally"/MAY sentences only).
- Fail-closed base (98991e6): `base_ref_error` rejects empty or `-`-prefixed
  bases and unresolvable refs via `rev-parse --verify --quiet
  --end-of-options <base>^{commit}` before any other step; the 3-case test
  also asserts no `leak` file is created. Called at main() before head/base
  are used.
- Validation file: `Ran 605 tests` / `OK`, `agent asset validation ok`,
  render `--check` via `uv run --with pyyaml` (the task's bare `python3` form
  lacks PyYAML on the host; the worker documented the substitution — task
  wording error, mine), guard self-run `guard exit 0`, line 408 fallback
  quoted, red-then-green proof of the new test (`FAILED (failures=3)` on
  fa934f7, `OK` on 98991e6).
- PR feedback evidence: 15 items for head 98991e6 (11 runner notices,
  1 Homebrew tap-trust warning, 2 bot notices, 1 CodeRabbit skipped status);
  every disposition is `not-applicable:` with a reason of 20+ characters; no
  review items exist, so the "no bot review" path is what the self-run
  exercised.
- CI: `gh pr checks 210` shows every check pass (nix skipping); confirmed by
  me after the auditor could not reach GitHub.
- Sandbox record: worker-c on `feat/pr-feedback-gate-r2`, clean after the
  copy-out; step-3 worktree artifacts deleted, not committed.
- Boundaries: no `.ua/`, hooks, settings or workflow files beyond the
  allowed ones; #182 untouched; no bot comments posted; no ruleset applied.
- CompactionDB: decision dca7d66a-2821-42e5-a48f-8bb89b444757 present
  (`memory list`).

## Codex audit dispositions

`herdr-agents --audit` audits one commit, so both substantive commits were
audited (the carry commit is verified by the byte-identity check above).

- 98991e6 (`…-audit.md`): no findings; approval notes fail-closed ordering,
  argument-list subprocess, regression coverage. "Live CI verification
  failed because GitHub was unreachable" → dispositioned: CI verified by the
  orchestrator (all checks pass). `Verdict: correct`.
- fa934f7 (`…-audit-fa934f7.md`): `Verdict: correct` (see file for the
  auditor's approval text).

Worker-side review findings: (1) fixed in 98991e6. (2) P2 BASE not bound to
the PR's GitHub base, (3) P3 evidence path excluded from diff sizing, (4) P3
`gh api -F` coercion → deferred to a security-lane follow-up task
(`security` profile Codex worker, identity `codex-security-dot`); all three
are quoted verbatim with file:line in the report.

## Review guard

crit-data evidence `dot-pr-feedback-gate-T38-a01-crit.json` (19 records, 19
resolved; approval r_fa36e9), receipt `…-receipt.md`; guard run recorded
below.

## Decision

**Decision: ACCEPTED** (2026-09-29). Merge PR #210 by squash without
`--delete-branch` (worker-c holds the branch); close #182 with a pointer to
#210. Operator-visible impact: the PR integration rule becomes active for
Claude and Codex after the next `make update`; `make require-crit-review`
gains `BASE`/`PR_FEEDBACK_EVIDENCE`; no CodeRabbit review is required and no
workflow posts review requests.

[memory:decision] T38 accepted: PR #182 lives on as #210 with an optional
CodeRabbit review, no auto-trigger, no Codex connector dependency, and a
fail-closed `--base`; findings (2)(3)(4) go to a security-lane task
(operator 2026-09-29).

cost: worker-reported 1 read-only review subagent (82,151 tokens); orchestrating session n/a; two audit-lane runs.

## Review guard record

```
$ AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dot-pr-feedback-gate-T38-a01-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
exit 0
```
