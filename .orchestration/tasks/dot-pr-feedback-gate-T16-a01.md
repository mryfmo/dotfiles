# AGMSG-TASK dot-pr-feedback-gate-T16-a01: mandatory GitHub feedback sweep, explicit CodeRabbit review, and merge gate (plan Phase G.1)

Plan: `.agents/worklog/claude/remediation-plan-20260925.md` §Phase G. Operator finding: PRs #178/#180 were merged without any bot review (CodeRabbit posts "fewer than 10 stars → manual trigger" on every PR and nobody triggered it) and with a failure-level check-run annotation nobody read. No rule or skill in dotfiles requires processing CI/bot feedback. This task closes that gap at the root: tooling that fetches everything, a rule that makes disposition mandatory, an automatic CodeRabbit trigger, and a guard that refuses integration without the evidence.

Repo: `/home/moriya/Workspace/dotfiles/.claude/worktrees/env-converge-T10`, branch `feat/pr-feedback-gate` from origin/main after T15 is pushed. You are `claude-standard-dot-a003`.

## Deliverables

1. **`scripts/pr-feedback.py`** (stdlib + `gh` CLI): `pr-feedback.py <pr-number> [--repo owner/name] [--json <out>]` collects, for the PR head sha: issue comments, PR reviews, inline review comments, review threads' resolution state (GraphQL `reviewThreads`), check runs with `conclusion` and every annotation (all levels: notice/warning/failure), commit statuses, and bot identities (`user.type == "Bot"`). Output one JSON document with a `items[]` list where each item has `source`, `author`, `level`, `path`, `line`, `body`, `url`, and an empty `disposition` field to be filled. Exit non-zero if `gh` is unauthenticated. Unit tests with recorded fixtures (no network in tests).
2. **Rule** `home/dot_config/claude/rules/pr-integration.md` (and the Codex mirror the repo uses for rules — find how other rules are mirrored, e.g. `home/dot_config/codex/AGENTS.md` sections) stating, as MUST: before merging any PR, run `pr-feedback.py`, trigger the bot review explicitly (`@coderabbitai full review`) and wait for its completion, give **every** item a disposition (`fixed:<commit>` with the root-cause fix, or `not-applicable:<reason>`; stopgaps are not a valid disposition), save the filled JSON under `.orchestration/validation/<task>-pr-feedback.json`, and summarise dispositions in the acceptance record. Bot annotations at level `failure` or `warning` are never left undispositioned. Add the same requirement to `home/dot_agents/skills/gh-first-workflow/SKILL.md` (Workflow + Output Checklist) and to the agmsg-orchestration SKILL Orchestrator Playbook (acceptance step).
3. **Automatic CodeRabbit trigger**: `.github/workflows/coderabbit-trigger.yml` — on `pull_request_target` `opened`/`ready_for_review` and on a manual `workflow_dispatch`/label (`review-requested`), a job with `permissions: pull-requests: write` posts `@coderabbitai full review` once per head sha (dedupe by a marker comment `<!-- coderabbit-trigger:<sha> -->`). **Do not trigger on every `synchronize`:** the repository's CodeRabbit plan allows 1 included review per hour (observed on PR #181: "Your plan provides up to 1 included review per hour; 0 remain after this review"). The rule therefore requires: one full review on the final head before merge (re-trigger only after the hour window, or use `@coderabbitai review` incremental if the docs confirm it is not counted the same way — verify and cite). Pin the action SHAs like the other workflows. Also add `.coderabbit.yaml` with `reviews.request_changes_workflow: true`, `reviews.path_filters` excluding `.orchestration/**`, `reviews/**`, `.ua/**`, and `language: ja-JP` for review text (keep code suggestions in English). Validate the YAML in CI (`validate` job).
4. **Merge gate**: extend `scripts/require-crit-review.py` (coordinate with plan 5.5 if already done; otherwise include the `--base <ref>` support here) to accept `PR_FEEDBACK_EVIDENCE=<json>` and fail when any item lacks a disposition or when a `failure`-level annotation is `not-applicable` without a reason ≥ 20 chars. Document in README "Agent Review Evidence" and AGENTS.md.
5. **Branch protection**: write `docs/` or README guidance (not executable here; repo admin action) for a ruleset on `main` requiring the `test`, `validate`, `public-bootstrap` checks and CodeRabbit's review status; record in the report that the operator must apply it (`gh api` command included).

## Tests
- `tests/unit/test_pr_feedback.py`: fixture-driven parsing of comments/reviews/annotations/threads; bot detection; disposition schema.
- `tests/unit/test_require_crit_review.py`: PR_FEEDBACK_EVIDENCE missing/incomplete/complete cases.
- Workflow lint: `actionlint` if available in the repo toolchain, else `yq` parse in the validate job.

## Validation (verbatim)
Unit tests; validator; `python3 scripts/pr-feedback.py 180 --json /tmp/...json` run against the real merged PR (read-only) and its item count; `gh pr checks` table.

## Commit / PR
Conventional commits; push `feat/pr-feedback-gate`; PR (English); **apply the new rule to this PR itself**: trigger `@coderabbitai full review`, wait, run `pr-feedback.py` on your own PR, fill dispositions, save JSON to `.orchestration/validation/dot-pr-feedback-gate-T16-a01-pr-feedback.json`, fix every actionable item at its root before RESULT.

## allowed_files
`scripts/pr-feedback.py`, `scripts/require-crit-review.py`, `.github/workflows/coderabbit-trigger.yml`, `.coderabbit.yaml`, `home/dot_config/claude/rules/pr-integration.md`, the Codex rules mirror file, `home/dot_agents/skills/gh-first-workflow/SKILL.md` (+ references), `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `README.md`, `AGENTS.md`, `tests/unit/test_pr_feedback.py`, `tests/unit/test_require_crit_review.py`, `.github/workflows/test.yaml` (validate job only), artefacts.

## forbidden_actions
merging; changing repo settings; `make update`/`make upgrade`/`chezmoi apply`; local bats; force-push.

## Artefacts
`.orchestration/<dir>/dot-pr-feedback-gate-T16-a01.md` ×5 + the pr-feedback JSON. `[memory:decision]`: "every PR integration requires a full GitHub feedback sweep (comments, reviews, threads, check-run annotations at all levels), an explicit CodeRabbit full review, and a root-cause disposition per item; evidence JSON is required by the integration guard". `contextdb_cli.py memory add`; paste.

## Done signal
`AGMSG-RESULT v1 task_id=dot-pr-feedback-gate-T16-a01 status=ready_for_review|blocked pr=<n> ...` via send.sh. max_turns=45.

## Scope approval (orchestrator, 2026-09-25 12:05Z)

Approved additions to allowed_files: `tests/unit/test_workflow_security.py` (one `EXPECTED_PERMISSIONS` entry for `coderabbit-trigger.yml: {pull-requests: write}`; repository policy requires top-level workflow permissions, so use top-level `permissions:` instead of job-level) and `home/dot_claude/rules/symlink_pr-integration.md.tmpl` (rule loading follows the same symlink-template pattern as every other rule). Pushing waits until #181 lands so the rebase needs no force-push (orchestrator will notify).

## Scope approval addendum (12:07Z)
(3) Approved: the YAML parse step for `.coderabbit.yaml` and `coderabbit-trigger.yml` goes into the `validate` job of `.github/workflows/agent-assets.yml` (`uv run --with pyyaml`); `actionlint` is not in the toolchain. Cite the CodeRabbit rate-limit docs in the rule text.
