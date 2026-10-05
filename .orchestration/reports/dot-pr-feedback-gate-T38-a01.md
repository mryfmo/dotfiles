# T38 report: PR feedback sweep + evidence-checked merge gate, CodeRabbit optional (dot-pr-feedback-gate-T38-a01)

- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: 9b4a40d289eb6cf78d0872e54262c80c79898053a5114ece37bc7e89a418a999 (sha256 verified against the main-checkout file and the `origin/main:` blob at 6fa41a5)
- branch: `feat/pr-feedback-gate-r2` from origin/main 6fa41a5. The task text says main is 20b8f88; 6fa41a5 is the orchestration commit on top of it. The merged local `chore/upgrade-pins-20260929` branch was deleted first, and the tree was clean.
- PR: https://github.com/mryfmo/dotfiles/pull/210 (head 98991e6, MERGEABLE; CI 12/12 pass, nix skipped; CodeRabbit "Review skipped: automatic reviews are disabled")
- `feat/pr-feedback-gate` / #182 were not touched and not closed.

## Commits

1. **f7433fc** `feat: carry PR #182 (PR feedback sweep and merge gate) onto main`
   - `git merge --squash origin/pr/182` (b25c005).
   - The only conflict was `AGENTS.md`. main's lines are kept verbatim, including the crit-fallback bullet and the whole `## Audit` section. The PR's "Before merging a pull request…" bullet is the last bullet of `## Agent Review Evidence`, before `## Audit`; `git diff origin/main -- AGENTS.md` shows exactly one added line.
   - Placement checks on the five auto-merged files:
     - README: the subsection follows the Crit paragraph.
     - Codex `AGENTS.md`: `## PR 統合` is its own section, before `## モデル選択`.
     - agmsg SKILL: the Orchestrator Playbook numbers run 1–11.
     - `crit-review.md` and the Makefile target are also correctly placed.
   - `make unit-test`: 604 OK.
2. **fa934f7** `feat(gate): make CodeRabbit optional and drop the review auto-trigger`
   - `scripts/require-crit-review.py`: removed `BOT_REVIEWER` and the mandatory bot-review check, and reworded the docstring. The head-match, base-collector, `fixed:` range, reason-length and multiset-coverage checks are unchanged.
   - `tests/unit/test_require_crit_review.py`: `test_pr_feedback_requires_a_completed_bot_review_of_head` is replaced by `test_pr_feedback_accepts_complete_evidence_without_a_bot_review`. The `bot_review()` fixture and its injection into `write_feedback` and the coverage, head-match and base-collector tests are dropped.
   - `tests/unit/test_pr_feedback.py`: `"@coderabbitai full review"` is removed from the parity TOKENS. The other tokens and all collector tests (with `coderabbitai[bot]` sample data) stay.
   - Rule and mirrors: `pr-integration.md` line 4 now says a `@coderabbitai full review` MAY be requested, a CodeRabbit review that exists is swept and dispositioned like any other item, and the gate does not require a bot review. The Convergence bullet is dropped. The same wording is in the Codex `## PR 統合` section (Convergence bullet dropped there too), the `AGENTS.md` bullet, agmsg SKILL step 10, and gh-first-workflow step 8 and its checklist.
   - README: the CodeRabbit step is marked optional, the paragraph saying the gate requires a coderabbitai review is replaced by "Bot-review presence is not gated", the trigger-workflow paragraph is replaced by "No workflow posts review requests automatically", and `CodeRabbit` is removed from the suggested ruleset's required checks.
   - Deleted `.github/workflows/coderabbit-trigger.yml`. The `agent-assets.yml` parse step now parses only `.coderabbit.yaml` (step renamed "Parse CodeRabbit config"), and its entry is removed from `test_workflow_security.py` EXPECTED_PERMISSIONS. `.coderabbit.yaml` is kept (auto review off).
   - `make unit-test`: 604 OK. validate ok; render ok.
3. **98991e6** `fix(gate): fail closed on an unresolvable --base` (orchestrator ruling fix-1, 09:13:19Z)
   - `base_ref_error()` runs `git rev-parse --verify --quiet --end-of-options <base>^{commit}` and rejects an empty or `-`-prefixed base. `main()` exits 1 with a clear message before any base diff, collector or `is-ancestor` use.
   - New test: `test_base_fails_closed_when_unresolvable_or_option_like`, covering `no-such-ref`, `--output=leak` and `""`. It fails 3/3 against fa934f7's guard (each ended in acceptance, exit 0) and passes on 98991e6.
   - `make unit-test`: 605 OK.

## Step 3: guard exercised on PR #210 (no bot review on the head)

- The collector does not exist on the base (`git show origin/main:scripts/pr-feedback.py` → exit 128), so `collected_feedback_errors` uses HEAD's own collector by design ("Prefer the base branch's collector; only a PR that introduces it has none", require-crit-review.py:408).
- The sweep ran after every check reached a terminal state: 15 items, **0 `review` items**. All 15 are dispositioned in `~/Workspace/dotfiles/.orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json`.
- `PR_FEEDBACK_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/claude/t38-receipt.md python3 scripts/require-crit-review.py --base origin/main` ended with "PR feedback evidence accepted", "Review requirement satisfied", and `guard exit 0`.
- The review evidence (crit-shape JSON `.agents/worklog/claude/t38-review.json` and receipt `t38-receipt.md`, gitignored in worker-c) records the independent subagent review: 4 findings plus 1 approval, all `resolved: true`, with `review_outcome: addressed`.
- The worktree copy of the pr-feedback JSON was removed after copying it to the main checkout. Nothing from step 3 is committed.
- No `@coderabbitai`/`@codex` comments were posted and no ruleset was applied.

### Every pr-feedback disposition (PR #210 @ 98991e6)

| # | source | author | level | url | disposition |
|---|---|---|---|---|---|
| 1 | issue_comment | coderabbitai[bot] | comment | https://github.com/mryfmo/dotfiles/pull/210#issuecomment-5887130583 | not-applicable:CodeRabbit status comment 'Review skipped' (auto reviews disabled by .coderabbit.yaml); it is not a review and contains no finding. Under this PR's gate a bot review is optional and none was requested. |
| 2 | issue_comment | chatgpt-codex-connector[bot] | comment | https://github.com/mryfmo/dotfiles/pull/210#issuecomment-5887148859 | not-applicable:chatgpt-codex-connector onboarding notice (no Codex account connected); not a review and no finding. The gate deliberately carries no Codex connector dependency. |
| 3 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138933/job/109339460572 | not-applicable:GitHub-hosted runner capacity notice about macOS arm64 queue times; informational runner status, not a finding about this change. |
| 4 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138933/job/109339460569 | not-applicable:GitHub runner-image notice that ubuntu-latest migrates to Ubuntu 26 from 2026-10-19; informational and repo-wide, not caused by this change. |
| 5 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138933/job/109339460535 | not-applicable:GitHub runner-image notice that ubuntu-latest migrates to Ubuntu 26 from 2026-10-19; informational and repo-wide, not caused by this change. |
| 6 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138987/job/109339402651 | not-applicable:GitHub runner-image notice that ubuntu-latest migrates to Ubuntu 26 from 2026-10-19; informational and repo-wide, not caused by this change. |
| 7 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402623 | not-applicable:GitHub-hosted runner capacity notice about macOS arm64 queue times; informational runner status, not a finding about this change. |
| 8 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402568 | not-applicable:GitHub runner-image notice that ubuntu-latest migrates to Ubuntu 26 from 2026-10-19; informational and repo-wide, not caused by this change. |
| 9 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402508 | not-applicable:GitHub runner-image notice that ubuntu-latest migrates to Ubuntu 26 from 2026-10-19; informational and repo-wide, not caused by this change. |
| 10 | annotation | github-actions | warning | https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402501 | not-applicable:Homebrew tap-trust warning for aws/tap, azure/bicep, hashicorp/tap that the macos-14 runner image pre-taps; it arises in the macos.yaml public-bootstrap job, which this PR does not change, and a fix belongs in macos.yaml (outside T38's allowed files; test.yaml:129 already trusts them for the unit-test job). |
| 11 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402501 | not-applicable:GitHub-hosted runner capacity notice about macOS arm64 queue times; informational runner status, not a finding about this change. |
| 12 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402414 | not-applicable:GitHub runner-image notice that ubuntu-latest migrates to Ubuntu 26 from 2026-10-19; informational and repo-wide, not caused by this change. |
| 13 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402248 | not-applicable:GitHub runner-image notice that ubuntu-latest migrates to Ubuntu 26 from 2026-10-19; informational and repo-wide, not caused by this change. |
| 14 | annotation | github-actions | notice | https://github.com/mryfmo/dotfiles/actions/runs/36548138933/job/109339402177 | not-applicable:GitHub runner-image notice that ubuntu-latest migrates to Ubuntu 26 from 2026-10-19; informational and repo-wide, not caused by this change. |
| 15 | status | coderabbitai[bot] | success | - | not-applicable:CodeRabbit success-state status reporting 'Review skipped: automatic reviews are disabled'; not a review. Bot-review presence is not gated by this PR. |

## Deferred findings (security-lane follow-up, per ruling)

The independent review found these in #182 code that step 1 carried unchanged. They are recorded as pre-existing and escalated in the crit evidence.

- **(2) P2 base-not-bound-to-pr-base**, `scripts/require-crit-review.py:405` (`collected_feedback_errors`): "Nothing ties BASE to the PR's actual GitHub base, so BASE=HEAD (or any commit on the PR branch) skips the protection. The base diff is then empty and `git show HEAD:scripts/pr-feedback.py` runs the PR's own, possibly tampered, collector. That collector can return `items: []` for the right head_sha, which defeats the claim that 'the PR under review cannot swap' the collector. Compare base against the PR's base ref/sha from the collected document, or pin the trusted collector to origin/<default branch>."
- **(3) P3 evidence-exclusion-any-path**, `scripts/require-crit-review.py:128` (`is_ignored`): "is_ignored drops whatever path PR_FEEDBACK_EVIDENCE names from review sizing, even a high-risk file such as .claude/settings.json or a JSON under scripts/. Without --base, the evidence only has to be `{\"items\": []}`, so a change to one high-risk JSON file plus that key can end in 'Review not required'. Limit the exclusion to .orchestration/validation/ or to paths that are not high-risk."
- **(4) P3 gh-graphql-F-coercion**, `scripts/pr-feedback.py:97`: "Every GraphQL variable is passed with `gh api -F`, which turns numeric or true/false strings into JSON numbers/booleans and reads `@file` values. An owner or repo name that is all digits breaks the `String!` variables, and `--repo @path` reads a local file. Use `-f` for the string variables (owner, name, cursor, id) and keep `-F` only for number."

Finding (1), P2 unverified-base-fails-open, is fixed in 98991e6 (see Commits).

## Notes

- The task's bare `python3 scripts/generate-agent-configs.py --check` fails with "PyYAML is required". The script's documented `uv run --with pyyaml` form passes; both outputs are pasted.
- `git grep 'codex review'` hits only README:596 and executable_herdr-agents:1502. Both are already on origin/main and say it is *not* used. No added line contains codex-review, connector or trigger text (the added-lines grep exits 1).
- The understand-anything auto-update hook fired after each commit. I did not act on it: `.ua/**` is forbidden in T38.

[memory:decision] T38: PR #182 is carried onto main as the PR feedback sweep
(`scripts/pr-feedback.py`) plus the evidence-checked merge gate
(`require-crit-review.py --base`, `PR_FEEDBACK_EVIDENCE`); CodeRabbit review is
optional (swept when present, never required), the auto-trigger workflow is
dropped, `.coderabbit.yaml` keeps auto review off, and the gate carries no
Codex GitHub connector dependency. Supersedes the T16 r2 Codex-gate ruling
(operator 2026-09-29).

## CompactionDB (main checkout)

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T38: PR #182 is carried onto main as the PR feedback sweep (scripts/pr-feedback.py) plus the evidence-checked merge gate (require-crit-review.py --base, PR_FEEDBACK_EVIDENCE); CodeRabbit review is optional (swept when present, never required), the auto-trigger workflow is dropped, .coderabbit.yaml keeps auto review off, and the gate carries no Codex GitHub connector dependency. Supersedes the T16 r2 Codex-gate ruling (operator 2026-09-29)."
dca7d66a-2821-42e5-a48f-8bb89b444757
```

## Effects

None outside the repository working tree. The review evidence lives in worker-c's gitignored `.agents/worklog/claude/`.

cost: 1 subagent dispatch (independent read-only review, 82,151 tokens as reported by the harness); orchestrating-session token/cost figures n/a.
