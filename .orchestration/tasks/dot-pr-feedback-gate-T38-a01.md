# AGMSG-TASK dot-pr-feedback-gate-T38-a01

## Objective

Revive PR #182 (`feat/pr-feedback-gate`, head b25c005, base 6026837) in a
reduced form and land it on today's `main` (20b8f88). PR #182 stalled on
2026-09-26: CodeRabbit hit its review rate limit, `@codex review` has no
connected connector, and the branch is 101 commits behind with an `AGENTS.md`
conflict. Operator decision 2026-09-29: keep the PR feedback sweep
(`scripts/pr-feedback.py`) and the evidence-checked merge gate
(`require-crit-review.py --base` + `PR_FEEDBACK_EVIDENCE`), make CodeRabbit
OPTIONAL, and carry no dependency on the Codex GitHub connector. This
supersedes the T16 revision-2 ruling (Codex review as the bot gate).

Deliver, in this order, as separate commits on one branch:

1. **Carry PR #182 onto main.** `git switch -c feat/pr-feedback-gate-r2 origin/main`
   then `git merge --squash origin/pr/182` (fetch the ref first:
   `git fetch origin refs/pull/182/head:refs/remotes/origin/pr/182`). The only
   textual conflict is `AGENTS.md`: keep every line main has (the crit-fallback
   bullet and the whole `## Audit` section verbatim) and place the PR's single
   "Before merging a pull request…" bullet as the last bullet of
   `## Agent Review Evidence`, before `## Audit`. Then review the five files
   that auto-merge for placement: `README.md` (the new "PR feedback and the
   merge gate" subsection must follow the Crit paragraph),
   `home/dot_config/codex/AGENTS.md` (`## PR 統合` must land as its own
   `## ` section before `## モデル選択` so the parity test's `split("\n## ")`
   isolates it), `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
   (Orchestrator Playbook numbering after inserting the new step),
   `home/dot_config/claude/rules/crit-review.md`, `Makefile`. Commit as
   `feat: carry PR #182 (PR feedback sweep and merge gate) onto main`.
   `make unit-test` must be green at this commit with the PR's own tests.
2. **Make CodeRabbit optional; remove the auto-trigger.**
   - `scripts/require-crit-review.py`: delete the `BOT_REVIEWER` constant and
     the hard "has no completed coderabbitai[bot] review of HEAD" check in
     `collected_feedback_errors` (PR lines 24, 396-401 docstring, 428-432).
     Keep the head-match, base-collector, `fixed:` range, reason-length and
     multiset-coverage checks unchanged: a CodeRabbit review that exists is
     collected and must be dispositioned like any other item; its absence is
     not an error.
   - `tests/unit/test_require_crit_review.py`: replace
     `test_pr_feedback_requires_a_completed_bot_review_of_head` with a test
     proving the guard ACCEPTS complete evidence when no bot review exists;
     drop the injected coderabbit fixture from the coverage tests where it
     only served the mandatory check.
   - `tests/unit/test_pr_feedback.py`: remove `"@coderabbitai full review"`
     from the parity TOKENS; keep the other parity tokens and all collector
     tests (sample data may still name `coderabbitai[bot]`).
   - Rules and docs: reword `home/dot_config/claude/rules/pr-integration.md`
     line 4 and its mirrors (`home/dot_config/codex/AGENTS.md` `## PR 統合`,
     `AGENTS.md` bullet, `agmsg-orchestration/SKILL.md` step,
     `gh-first-workflow/SKILL.md` step 8 + checklist, README) to: a
     `@coderabbitai full review` MAY be requested on the final head; when a
     CodeRabbit review exists it is swept and dispositioned like any other
     item; the gate does not require a bot review. Drop the "Convergence"
     bullet (line 8) and its mirrors. In README remove `"CodeRabbit"` from the
     suggested ruleset's required checks and the paragraph that says the gate
     requires a coderabbitai review; state instead that bot-review presence is
     not gated. Never add `@codex review`, `chatgpt-codex-connector` or
     `codex review` logic anywhere.
   - Delete `.github/workflows/coderabbit-trigger.yml` (auto-posting a review
     request on every PR contradicts "optional" and is what exhausted the
     rate limit); remove its path from the `agent-assets.yml` YAML-parse step
     (keep parsing `.coderabbit.yaml`) and its entry from
     `tests/unit/test_workflow_security.py` EXPECTED_PERMISSIONS. Keep
     `.coderabbit.yaml` (auto review disabled; a manual request still works).
   Commit as `feat(gate): make CodeRabbit optional and drop the review auto-trigger`.
3. **Exercise the new guard code on its own PR (validation, not the
   integration gate).** The orchestrator's acceptance-time
   `make require-crit-review` remains the authoritative gate; this step only
   proves the new code path end to end. On the base branch the collector does
   not exist yet, so `collected_feedback_errors` falls back to HEAD's own
   `scripts/pr-feedback.py` by design ("only a PR that introduces it has
   none"); paste the fallback line from the code in the validation file.
   The guard resolves `PR_FEEDBACK_EVIDENCE` inside the git toplevel of the
   cwd, so write the JSON INSIDE the worktree first, then copy it to the
   artifact path:
   `python3 scripts/pr-feedback.py <pr> --json .orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json`
   (worktree-relative), fill every disposition, then run
   `PR_FEEDBACK_EVIDENCE=.orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> python3 scripts/require-crit-review.py --base origin/main`
   with a hand-written-shape crit JSON plus receipt as `AGENTS.md` "Agent
   Review Evidence" permits (both also inside the worktree under
   `.agents/worklog/claude/`). The run must end in acceptance (exit 0) with NO
   bot review present on the head; paste it verbatim. Afterwards copy the
   pr-feedback JSON to the main checkout at
   `~/Workspace/dotfiles/.orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json`
   and do not commit the worktree copies. Do not post `@coderabbitai` or
   `@codex` comments.

[memory:decision] T38: PR #182 is carried onto main as the PR feedback sweep
(`scripts/pr-feedback.py`) plus the evidence-checked merge gate
(`require-crit-review.py --base`, `PR_FEEDBACK_EVIDENCE`); CodeRabbit review is
optional (swept when present, never required), the auto-trigger workflow is
dropped, `.coderabbit.yaml` keeps auto review off, and the gate carries no
Codex GitHub connector dependency. Supersedes the T16 r2 Codex-gate ruling
(operator 2026-09-29).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c feat/pr-feedback-gate-r2 origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.
- Do NOT push to `feat/pr-feedback-gate` and do NOT close #182; the
  orchestrator closes it at acceptance with a link to your PR.

## Allowed files

- `scripts/pr-feedback.py`, `scripts/require-crit-review.py`, `Makefile` (require-crit-review target only)
- `tests/unit/test_pr_feedback.py`, `tests/unit/test_require_crit_review.py`, `tests/unit/test_workflow_security.py` (one entry only)
- `home/dot_config/claude/rules/pr-integration.md`, `home/dot_claude/rules/symlink_pr-integration.md.tmpl`, `home/dot_config/claude/rules/crit-review.md`, `home/dot_config/codex/AGENTS.md`, `AGENTS.md`, `README.md`
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_agents/skills/gh-first-workflow/SKILL.md`
- `.coderabbit.yaml`, `.github/workflows/coderabbit-trigger.yml` (arrives with the carry commit, deleted in the second commit), `.github/workflows/agent-assets.yml` (the parse step only)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-pr-feedback-gate-T38-a01*.md|json` (main checkout), `.agents/worklog/**` (review evidence)

## Forbidden actions

- Any other `.github/workflows/*`; `home/dot_claude/settings*`, `.claude/hooks/**`, permgate; `.ua/**`; `.orchestration/tasks/**` and the T16 task/acceptance records; main's `## Audit` section in `AGENTS.md`.
- Adding `@codex review` / connector / `codex review` logic; posting `@coderabbitai` or `@codex` PR comments; applying any ruleset via `gh api`; force push; pushing to `feat/pr-feedback-gate`; merging or closing PRs; local bats; `make update`/`upgrade`; writes outside the worktree except the listed paths.

## Validation commands (paste verbatim output)

```
git merge-base --is-ancestor origin/main HEAD && echo base-ok
git diff --stat origin/main
make unit-test
make validate-agent-assets
python3 scripts/generate-agent-configs.py --check
git grep -n -e 'codex review' -e 'chatgpt-codex-connector' -e 'coderabbit-trigger' -- ':!.orchestration' ; echo "grep exit $?"
PR_FEEDBACK_EVIDENCE=.orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> python3 scripts/require-crit-review.py --base origin/main ; echo "guard exit $?"
gh pr checks <pr-number>
```

## Completion

1. PR to `main` titled `feat: PR feedback sweep and evidence-checked merge gate with optional CodeRabbit (supersedes #182)`, English description that credits PR #182, lists what changed versus it (optional CodeRabbit, trigger dropped), and ends with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs, the PR number and head SHA; the report lists every disposition in the pr-feedback JSON.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `send.sh --body-file` for replies (turn delivery reaches you).
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
