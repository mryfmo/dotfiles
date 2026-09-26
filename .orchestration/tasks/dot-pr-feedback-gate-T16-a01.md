---
task_id: dot-pr-feedback-gate-T16-a01
revision: 2
---
# AGMSG-TASK dot-pr-feedback-gate-T16-a01 (revision 2): mandatory GitHub feedback sweep, Codex review as the bot gate, merge gate (plan v2 P3)

Revision 2 replaces revision 1 entirely. Operator decision 2026-09-26T02:58Z: **CodeRabbit is removed from the gate; Codex review replaces it.** Reason: CodeRabbit's included limit is one review per hour per repository, which serialized every PR round onto a wall clock; Codex cloud review already ran on this repo (PRs #172–#177) without such a limit.

Repo: `/home/moriya/Workspace/dotfiles/.claude/worktrees/env-converge-T10`, branch `feat/pr-feedback-gate` (PR #182, head b25c005). You are `claude-standard-dot-a003`. Rebase onto origin/main (3375fb0 or later) first.

## Facts (verified by the orchestrator from GitHub data, 2026-09-26 03:0xZ)
- `chatgpt-codex-connector[bot]` posted a Codex PR review on every PR authored by `mryfmo` (#172–#177): one issue comment carrying the markers `<!-- codex-pull-request-review-summary -->` and `<!-- codex-security-review:v1 {"blockingSeverityThreshold":"P0","headSha":"<sha>", …} -->`, plus inline review comments with `P1`/`P2` badges. It reviewed none of #178–#184 (author `moriya-fumio-thd`, the only gh account on this host).
- Probe 03:01:46Z: `@codex review` on #182 from `moriya-fumio-thd` → connector replied 03:01:49Z "To use Codex here, create a Codex account and connect to github". The connector is bound to the `mryfmo` account; enabling it for this host's account is an operator action (gh login as `mryfmo`, or connecting `moriya-fumio-thd` at chatgpt.com/codex/cloud/settings/connectors). Your self-application (deliverable 6) may therefore be blocked on the operator; report it as such with the connector's reply pasted, do not work around it.
- Codex CLI 0.157.0 has `codex review [--uncommitted|--base <ref>]` (non-interactive). It is not logged in on this host; treat it as an optional local equivalent, never as the gate.

## Deliverables
1. **`scripts/pr-feedback.py`** — keep as in revision 1 (stdlib + `gh`; issue comments, reviews, inline comments, thread resolution via GraphQL, check-run annotations at every level; bot detection generic; disposition schema; `--json`). Add: recognise the Codex summary marker and expose `codex_review: {head_sha, summary_comment_id, blocking_threshold}` for the PR head; `--require-codex-review` exits non-zero when no summary exists for the current head.
2. **Rule** `home/dot_config/claude/rules/pr-integration.md` + the Codex rules mirror + `gh-first-work` skill text: MUST before merge — full sweep, every item dispositioned, **a Codex review summary for the final head** (trigger with an `@codex review` comment if the automatic review did not run; wait for the summary; re-request after every push), evidence JSON saved under `.orchestration/validation/`. Remove every CodeRabbit sentence.
3. **Remove CodeRabbit**: delete `.coderabbit.yaml`, `.github/workflows/coderabbit-trigger.yml`, the `EXPECTED_PERMISSIONS` entry and the YAML-parse step added for them, and every CodeRabbit reference in rules/skills/README/tests on this branch. Document in README (repo admin section) that the CodeRabbit GitHub App is to be uninstalled from the repository (operator action) and that Codex review requires the PR author's GitHub account to be connected to a Codex account.
4. **Merge gate**: `scripts/require-crit-review.py` accepts `PR_FEEDBACK_EVIDENCE=<json>`, fails when any item lacks a disposition, when the evidence head ≠ the PR head, or when `codex_review.head_sha` ≠ head (unless `PR_FEEDBACK_ALLOW_NO_CODEX=1` with a reason string, logged into the receipt — for repositories where the connector is not connected).
5. **Branch protection guidance** (docs, not executable): required checks `test`, `validate`, `public-bootstrap`; note that Codex review has no GitHub check status, so the gate is enforced by `require-crit-review` evidence.
6. **Self-application**: rebase, push, comment `@codex review`; if the connector replies "create a Codex account", paste the reply into the validation file and send `status=blocked` with `blocker=operator:codex-connector-not-connected-for-<account>`; otherwise wait for the summary, run `pr-feedback.py 182 --json --require-codex-review`, disposition every item, fix findings in one consolidated round, save the JSON at `.orchestration/validation/dot-pr-feedback-gate-T16-a01-pr-feedback.json`.

## Tests
- `tests/unit/test_pr_feedback.py`: fixtures from the real #173 connector comment shape (summary marker + inline `P1`/`P2` comments); `--require-codex-review` pass/fail; head mismatch.
- `tests/unit/test_require_crit_review.py`: evidence missing/incomplete/complete; codex head mismatch; `PR_FEEDBACK_ALLOW_NO_CODEX` path writes the reason into the receipt.
- `tests/unit/test_workflow_security.py`: the CodeRabbit workflow entry is gone.

## Validation (verbatim)
Unit tests; validator; `python3 scripts/pr-feedback.py 173 --json <path>` against the real merged PR (read-only) showing `codex_review.head_sha`; `gh pr checks 182` table; the `@codex review` exchange on #182.

## allowed_files
`scripts/pr-feedback.py`, `scripts/require-crit-review.py`, `.coderabbit.yaml` (delete), `.github/workflows/coderabbit-trigger.yml` (delete), `.github/workflows/agent-assets.yml` (revert the YAML-parse step), `home/dot_config/claude/rules/pr-integration.md`, the Codex rules mirror file, `home/dot_agents/skills/gh-first-work/**`, `README.md` (PR integration + repo admin sections), `tests/unit/test_pr_feedback.py`, `tests/unit/test_require_crit_review.py`, `tests/unit/test_workflow_security.py`, `.orchestration/**/dot-pr-feedback-gate-T16-a01*`.

## forbidden_actions
merging; changing repo settings or GitHub App installations; `gh auth` changes; `codex login`; `make update`/`make upgrade`/`chezmoi apply`; local bats; force-push; any `@coderabbitai` comment.

## Artefacts / Done signal
Standard five + pr-feedback JSON + crit JSON on the branch. `[memory:decision]`: "every PR integration requires a full GitHub feedback sweep with dispositions and a Codex review summary for the final head; CodeRabbit is retired." `AGMSG-RESULT v1 task_id=dot-pr-feedback-gate-T16-a01 status=ready_for_review|blocked report=<path> validation=<path> pr=182` via send.sh. max_turns=45.

## Revision history
- r1 (09-25 12:05Z, + scope approvals 12:05Z/12:07Z): CodeRabbit explicit trigger + workflow.
- r2 (09-26 03:05Z): CodeRabbit removed per operator decision; Codex review summary is the bot gate; connector-account blocker documented.
