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

## Revise round 1 (task_rev 4ba1a66b…) and follow-ups

The final head is `4656f19f2183467052aa010e741e4df73bc663d8`. CI: all 13 checks pass, and the branch is up to date with main 680b29b1. The Codex Bot gave no review of this head between the 12:32:49Z push and 12:48:29Z (`bot: none`, listing pasted).
- **`126513d4`, round 1, P2.** The headless audit removes `<out>` and `<out>.last.md` first, runs under `set -o pipefail`, treats a nonzero codex exit as no audit (rerun), and masks only after a zero exit.
- **`c2660469`.** main merged T93 (#251) through update-branch, so the SKILL no longer calls T93 pending. It says to mask the audit evidence and the PR-feedback JSON with `--mask-secrets` before committing them, and that the gate compares feedback bodies after the same masking.
- **`4656f19f`, Codex review of 36086f48:**
  - 4177560247 (P1): the headless masker runs from a trusted checkout and is refused, like herdr-agents does, when HEAD is the audited commit or the validator is missing, untracked or changed. A refused or failed masking fails the audit, so a PR can never run its own validator on the orchestrator.
  - 4177560241: the headless prompt carries the pair form's task-level inputs (task file, worker artifacts, feedback JSON, head, merge-base PR diff) and asks for `[P0-P3]` findings plus one Verdict line.
  - 4177560255: the step-15 queries match the final head, reviews by `commit_id` and findings by `original_commit_id`, because a comment's `commit_id` moves to the newest head (visible in the listing).
- Update-branch merges `af305848` (main 2e2e1e09, #251) and `36086f48` (main 680b29b1, #255 boundary commit).
- Local checks on 4656f19f: `make unit-test` 785 OK, `make validate-agent-assets` ok, the docs and herdr-agents tests OK, prettier clean.

Proposed dispositions for the new threads:
- 4177560241 → `fixed:4656f19f`
- 4177560247 → `fixed:4656f19f`
- 4177560255 → `fixed:4656f19f`
- Earlier threads as in the table above.

Reporting note: `executable_herdr-agents:2159` still prints "or run codex --profile audit review headless" when no managed workspace exists. T69 allowed only the one string at line 1133, so this second stale hint is left for a follow-up.

## Revise round 2 (task_rev 40def5a7…)

Fix commit `6b060ac4`; this is the final head. CI: all 13 checks pass, and the branch is up to date with main 680b29b1.
1. **Facts in one place.** `AGENTS.md` (Audit), `README.md:292`, `model-selection.md:3` and gh-first-workflow step 8 now point to the SKILL's task-level audit bullet and Orchestrator Playbook step 10. GNU grep finds no `herdr-agents --audit` in them, except README:762, the existing helper reference section. gh-first-workflow keeps the sweep, disposition and gate tokens because `tests/unit/test_pr_feedback.py` (out of scope) pins them.
2. **Evidence.** The "reordered" grep output came from this shell's `grep`, a function wrapping ugrep 7.8.4, which prints parallel matches out of operand order. Both checks are recaptured on the final head with `/usr/bin/grep` (GNU grep 3.11), and the earlier blocks are marked superseded.
3. **Worker Playbook step 4** states the exception until dotfiles-T97: a Claude seat runs its GitHub calls (`git fetch`, `git push`, `gh`) outside its sandbox through the permission gate. Every other out-of-sandbox action stays a blocked PONG, and a Codex seat never leaves its sandbox.
   - Deviation from the round text: it says GitHub calls are the *only* unsandboxed commands. In practice this task's main-checkout CompactionDB `memory add` also ran unsandboxed, because that state directory is read-only from a worktree sandbox, and `agmsg-dispatch` runs outside it via `excludedCommands`. Step 4 names both, so it states what happens.

The Codex review of 6b060ac4 (13:11:05Z) raised P2 **4177767259**: `executable_herdr-agents:2159`, the no-workspace branch of `--audit`, still says "run codex --profile audit review headless". It is valid; I flagged the same string last round. T69 allows exactly one string in that file (line 1133), so it is not changed here. Proposed: allow that second string in this PR, rewording it to point to the SKILL's headless form, or hand it to a follow-up. Decision left to the orchestrator.

## Round-2 addenda (task_rev e054a70f…, 1b6220c2…)

The addenda arrived while round 2 was being pushed, so they are in a follow-up commit, `fdb938ad`, rather than the same one. That is the final head: CI all pass, up to date with main 680b29b1, and no Bot review on it within 15 minutes (`bot: none`, listing pasted).
- **Step 4.** It uses the addendum's wording: GitHub calls are the one class of commands a Claude seat runs outside its sandbox, through the permission gate, because the sandbox's existing GitHub domain allowance (`claude.sandbox.network.allowedDomains`, pasted) does not make `gh`/`git push` work there yet. dotfiles-T97 ends the exception. It no longer claims the allowance is missing, and it keeps naming the main-checkout `memory add` and `agmsg-dispatch` as the two documented out-of-sandbox cases.
- **Step 2.** A seat creates the branch with `git switch -c <branch> --no-track origin/main`, pushes with `git push origin <branch>` (no `-u`) and opens the PR with `gh pr create --head <branch>`, because the shared `.git/config` is read-only for a Codex seat. A Claude seat's sandbox produced the same `config.lock` failure in this session, so the sentence covers both. The orchestrator removes a leftover `.git/config.lock`.

Thread 4177767259 (`herdr-agents:2159`) is still awaiting the orchestrator's scope decision.

## Revise round 3 and round-3 addendum (task_rev e48f28cc…)

Commits: `0b65a2ec` (round 3) and `d9bbd800` (formatting fix). The update-branch merge `29ea2528` brought in main 2ad504e3 (#256). The final head is `d9bbd800`: CI all pass, the branch is up to date with main 2ad504e3, and no Bot review or new Bot finding arrived on it within 15 minutes (`bot: none`; head-filtered listing pasted).

- **Thread 4177767259 (in scope per the round-3 decision).**
  - `executable_herdr-agents:2159`, the no-workspace path of `--audit`, now says "…or run the audit headless as the agmsg-orchestration SKILL task-level audit bullet shows ("codex <audit profile args> exec --sandbox read-only -C <repo> -o <out>.last.md <prompt>")."
  - It is a string-only change, matching line 1133. The pin is `tests/unit/test_herdr_agents.py:5067`.
  - Proposed disposition: `fixed:0b65a2ec`.
- **Formatting slip.**
  - The pin added in 0b65a2ec exceeded ruff's line limit. CI's "Check Python and Markdown formatting" step failed on 0b65a2ec and on 29ea2528.
  - I had run the unit tests, but not `ruff format --check`, before pushing.
  - `d9bbd800` is `ruff format` of that one line. The full ruff check is now part of the pasted final-head block.
  - This makes two commits for round 3, not the one asked for.
- **Addendum item 1 (evidence).** The validation file's round-3 section pastes each exact invocation with its output tail and `; echo "rc=$?"` on d9bbd800:
  - the docs and herdr-agents modules with `-v`: 235 = 6 + 229, reconciled per module;
  - prettier;
  - ruff;
  - `make unit-test`: 787 OK, with the same single skip;
  - `make validate-agent-assets`: ok, exit status captured without a pipe.
- **Addendum items 2 and 3.** No change: the gh-first-workflow step 8 literal stays, and the pr-feedback snapshot belongs to the orchestrator.
- **task_rev.** The round-3 dispatch named an earlier task-file revision. The only addition since then is the "Round 3 addendum" section, and the current sha256 is e48f28cc… (pasted).
