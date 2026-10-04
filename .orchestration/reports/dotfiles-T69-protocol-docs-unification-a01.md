# dotfiles-T69-protocol-docs-unification-a01 — report (status: ready_for_review)

Worker: `claude-standard-dot-a006` (Claude Code, `standard`), worktree `.claude/worktrees/worker-d`.
PR: https://github.com/mryfmo/dotfiles/pull/253 — branch `docs/protocol-unification` from `origin/main` febd0cb7.

Commits:
- `acb1b93c` task
- `4e83dd8d`, `3c6a3cb2`, `d31dc32d` Codex review fixes
- update-branch merges `82611f39` (main 6de95167, #252) and `0d9cb61a` (main c6b348ba, #254)

Final head `d31dc32d0a5a0fceceab81d5f8f0d2d9a28e4437`:
- CI: all 13 checks pass, and the branch is up to date with main c6b348ba;
- `mergeable_state` = `blocked` because the Bot threads are unresolved; the worker resolves none.

Task file `40b66d86…` verified.

## Changes (allowed files only)

1. **Audit command.** The agmsg-orchestration SKILL's new "Task-level audit" bullet (replacing the per-commit pre-screen) names both forms once.
   - Pair form: `herdr-agents --audit <head-sha> --task <id> [--out <path>] <main DIR>`. It writes `.orchestration/validation/<id>-audit-<sha7>.md`, with the verdict in the `.last.md` companion.
   - Headless form: `codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <repo> -o <out>.last.md '<prompt>' 2>&1 | tee <out>`, then `scripts/validate-agent-assets.py --mask-secrets <out> <out>.last.md`.

   These point to that bullet instead of restating the command: the SKILL's pane-less bring-up and delegation bullets, the agmsg-orchestration rule, `model-selection.md:3` (its `model_profiles`, `express-explorer` and `review` tokens are intact), `AGENTS.md` (Audit and Agent Review Evidence), `README.md:292` and `:559`, and the `herdr-agents` pane-less hint string (one string, `bash -n` clean, with its `test_herdr_agents.py` expectation). `codex --profile audit review --commit` is written nowhere; only README's sentence explaining why `codex review --commit` is not used remains.
2. **One audit per task.** The pre-screen sentences in the SKILL and the rule are gone.
   - The audit of the final head covers the whole PR diff (`git diff <merge-base> <head>`), and a new push, including `gh pr update-branch`, needs a new audit.
   - It runs from a clean tree, or from a dedicated clean checkout.
   - Every `[P0-P3]` finding gets an `audit-finding: <n> …` line starting at column one, whatever the verdict. A `fixed:<sha>` needs a fresh audit, and the gate checks `not-applicable:` for an `incorrect` verdict (T68).
   - Evidence masking (T93) is named as pending: it was not merged at this branch point.
3. **Integration order.** Orchestrator Playbook step 10 is the single procedure: sweep → task-level audit → acceptance record → gate → `gh pr merge --squash` → `AGMSG-ACCEPTANCE`.
   - The gate is `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=…] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
   - It repeats after every update-branch.
   - An `incorrect` exit from `herdr-agents --audit` continues to the acceptance record; a `blocked` or missing verdict re-runs the audit.
   - `AGENTS.md:51`, `gh-first-workflow` step 8, the Codex `AGENTS.md`, `README.md` (the guard block and the PR-integration example, which includes the conditional `AUDIT_DISPOSITIONS`) and the `Makefile` comment cite step 10 and the pr-integration rule.
4. **Worker Bot wait (Worker Playbook step 15).**
   - `gh pr checks <pr> --watch`, then `gh api --paginate …/pulls/<n>/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'` and the Bot's top-level `…/pulls/<n>/comments` (`in_reply_to_id == null and .user.type=="Bot"`). Repeat until a review of the final head appears or 15 minutes pass (`bot: none`).
   - A 👍 reaction alone is not a review. P0/P1 findings are fixed with a fix commit and the wait starts over. The RESULT names every unresolved thread; the worker resolves none.
   - The wait is the named, permitted exception to the no-polling rule: at most every 30 seconds, no bare foreground `sleep`.
   - VERIFY: the field names were checked against the GitHub REST docs and live PR #243 data (pasted). Both endpoints page at 30 by default, hence `--paginate`.
5. **Boundary PR.** `pr-integration.md` and the Codex "PR 統合" mirror say a boundary PR is merged with `gh pr merge --squash --auto` without running `make require-crit-review`, so it needs no sweep JSON and no audit. Its Bot threads get a disposition reply and are resolved, and the next boundary commit message names the PR.
6. **Tests.** `test_agmsg_orchestration_docs` pins `--audit`, `--task`, `-audit-<sha7>.md`, `AUDIT_EVIDENCE`, `in_reply_to_id` and the Bot-wait phrase in both the rule and the SKILL. It also asserts that `review --commit` is absent from `AGENTS.md`, `README.md` (except the explanatory sentence), the rule, the SKILL and `model-selection.md`.

The T88 parallel-execution, routing-by-boundary and step-14 text is cited, not rewritten. Rule word count: 1269 before T88, now ~1650; T83 owns the diet.

## Codex review threads (all from chatgpt-codex-connector[bot]) and proposed dispositions

| Thread | Raised on | Finding | Disposition |
| --- | --- | --- | --- |
| 4177126680 | acb1b93c | Bot wait needs a permitted wait mechanism | `fixed:4e83dd8d` |
| 4177126683 | acb1b93c | audit from a clean checkout | `fixed:4e83dd8d` |
| 4177126686 | acb1b93c | headless audit must write `<out>` | `fixed:4e83dd8d` |
| 4177126689 | acb1b93c | disposition findings under a `correct` verdict | `fixed:4e83dd8d` |
| 4177157846 | 82611f39 | boundary PR vs the gate's feedback requirement | `fixed:3c6a3cb2` |
| 4177157848 | 82611f39 | mask headless audit artifacts | `fixed:3c6a3cb2` |
| 4177157852 | 82611f39 | README example lacks `AUDIT_DISPOSITIONS` | `fixed:3c6a3cb2` |
| 4177247697 | 0d9cb61a | continue after an `incorrect` audit exit | `fixed:d31dc32d` |
| 4177247706 | 0d9cb61a | duplicate of 4177247697 | `fixed:d31dc32d` |
| 4177247710 | 0d9cb61a | filter the comment wait to Bot authors | `fixed:d31dc32d` |

Final head d31dc32d: no Bot review between the ~11:24Z push and 11:39:34Z (step-15 listing pasted), so `bot: none`.

## Reporting notes

- **Pinned gate literal.** `tests/unit/test_pr_feedback.py` (not in allowed_files) pins the literal `BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review` in both skills. The documented gate command therefore puts the audit variables first; environment assignments are order-free. A future task owning that test could pin the audit variables too.
- **Stale CompactionDB memory.** `5b258cc8` says parallel execution is "to be written … by dotfiles-T69"; T88 already wrote it. The orchestrator may want to retract or update it at consolidation.

[memory:decision] dotfiles-T69 (operator 2026-10-03): the written protocol names one audit per task on the final head via `herdr-agents --audit <sha> --task <id>` (headless `codex … exec --sandbox read-only` otherwise), the acceptance order sweep → audit → acceptance record → gate with `AUDIT_EVIDENCE` → merge → ACCEPTANCE, the worker's Bot-wait by listing reviews of the final head, and the boundary PR as a sweep-free, audit-free exception; `codex --profile audit review --commit` is no longer written anywhere.

CompactionDB: the exact command and UUID `784fed94-42f9-4daf-8f1c-5f1f2fa53214` are in the validation file.

cost: n/a (the Claude Code runtime does not expose per-session token or cost figures to the worker)
