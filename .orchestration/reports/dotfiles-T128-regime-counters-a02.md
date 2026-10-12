# Report: dotfiles-T128-regime-counters-a02 (reset continuation of a01, plan 006 Phase A3)

- Worker `claude-standard-dot-a004`, worktree `.claude/worktrees/worker-c`, branch `feat/regime-counters`, PR #319 (open and ready), continuing from `72764f05` (a01's last head) under the reset record `.orchestration/acceptance/dotfiles-T128-regime-counters-a01-design-reset.md`.
- Commits after `72764f05`: `37267e90` copies the task file byte-identical to `.orchestration/dotfiles-T128-regime-counters-a02/task.md` (sha256 `afc46c3b…`, the `…-a01/` directory stays). `3ea405c8` is the one content commit and the final head.
- a01's report (`.orchestration/reports/dotfiles-T128-regime-counters-a01.md`) stays the record for everything a02 does not change: the design of both scripts, the fixture figures against baseline.md, the Bot rounds on PR 319 so far, and the local test environment.

## What a02 changes (the reset's three items, nothing else)

1. **First-token status and verdict (audit P1).** A message's status and verdict are its first `status=` and `verdict=` tokens, read with `tok()` like `task_id`. `has()` over the whole body is deleted. questions = `tok("status") == "question"`, withdrawn = `tok("status") == "withdrawn"`, a reset accept = `tok("verdict") == "accept"` (scripts/regime-counters.sh:112, :113, :117). The fixture figures are unchanged: T119 10/9/8/6/5, T124 W1 questions 6, V0 withdrawn 1, T118 revises 9.
2. **The `reset_of` binding (audit P1).** A reset record anchors only when three things hold:
   - its `design_sha256:` is the sha256 of its `redesign_task:` file;
   - that file's front-matter `reset_of` names the task being reset;
   - an identity other than the task's TASK senders sent `verdict=accept` for that hash.

   `reset_of` is read with PyYAML through `uv run --no-project --with pyyaml`, the repository's existing idiom (Makefile `validate-agent-assets`, `render-check`); there is no hand-written YAML parser (design R2, INV-1). uv runs `--offline` first, using the cached wheel, and online only when uv itself fails: a cold CI cache has network but no wheel, while a sandbox has the wheel but no network once pypi's index revalidates. Python always prints yes or no and catches an unreadable or malformed file, so only a uv failure triggers the fallback, and any failure is a no (scripts/check-regime-boundary.sh:216-233, :248-250). Both real forms anchor live:
   - a01's record names a02, whose `reset_of` is an inline list `[dotfiles-T128-regime-counters-a01]`; a01 is absent from the live boundary output;
   - both T124 records name `dotfiles-T128-regime-v3-a01`, whose `reset_of` is a block list; only their `waiver-unanchored` lines remain, with no S2 lines.

3. **The fixture budget (audit P2).** `pr-313.json` and `pr-317.json` now hold only the Codex P0/P1 top-level comments (31 and 14) and the commits (12 and 17), one object per line, with only `user.login`, `in_reply_to_id`, `original_commit_id`, `body` (the title line) and `sha`. The message TSVs were already only the task's rows: the first-`task_id=` filter removed none. `git diff --numstat origin/main -- tests/ | awk '{a+=$1} END {print a}'` gives **931** (validation file), down from 1735.

Tests added for the reset's rows:

- `tests/unit/test_regime_counters.py::RegimeCountersTest::test_a_status_in_free_text_counts_nothing` covers a PONG `status=blocked` noting `status=question`, an ACCEPTANCE `status=accepted` noting `status=withdrawn`, and a RESULT `verdict=revise` noting `verdict=accept` with the hash.
- `tests/unit/test_check_regime_boundary.py::RegimeBoundaryCountsTest::test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing` covers T9's redesign accepted under its genuine hash, which anchors nothing for T1. The same design with a block-list `reset_of` naming T1 does anchor.
- `test_a_reset_record_silences_only_when_another_identity_accepted_its_design` gains a case: another accepted hash named for T1-redesign, whose `reset_of` does name T1, anchors nothing. This keeps the hash rule load-bearing next to the new binding.

## invariant lines (final head `e87a52fc`, after amendment 1)

- invariant: INV-6 → scripts/regime-counters.sh:48 (INV-6's constant 2 for every count)
- invariant: INV-6 → scripts/regime-counters.sh:85 (the whole team history through `storage_history`; schema guard :83)
- invariant: INV-6 → scripts/regime-counters.sh:103 (task = first `task_id=` token)
- invariant: INV-6 → scripts/regime-counters.sh:112-113 (questions and withdrawn from the first `status=` token)
- invariant: INV-6 → scripts/regime-counters.sh:141 (amendments = TASKs − 1; revises = RESULTs − 1, no status excluded)
- invariant: INV-6 → scripts/regime-counters.sh:114 (first RESULT's `head=`)
- invariant: INV-6 → scripts/regime-counters.sh:115 (the task's PR: digits, `none`, or `invalid`; only digits fetched)
- invariant: INV-6 → scripts/regime-counters.sh:132-137 (Codex Bot P0/P1 heads after the first RESULT head in PR commit order; `unknown`, never 0)
- invariant: INV-6 → scripts/regime-counters.sh:92 (`gh api --paginate`)
- invariant: INV-6 → scripts/regime-counters.sh:117 (design accepted in a RESULT whose task is the record's `redesign_source` (`--reset-source`), by the first `verdict=` token, from an identity other than the TASK senders)
- invariant: INV-6 → scripts/check-regime-boundary.sh:252-260 with :216-241 (reset record: the redesign file's hash, its `reset_of`, a foreign accept)
- invariant: INV-6 → scripts/check-regime-boundary.sh:282 (accepted record anchored on the task's merged PR) and :284-285 (`pr=none` only for a format-2 review or design task file whose RESULTs carry no `pr=`; front matter read at :237)
- invariant: INV-6 → scripts/check-regime-boundary.sh:293-295 (a `DESIGN_RESET_WAIVED_BY=` line silences nothing: `waiver-unanchored`)
- invariant: INV-6 → scripts/check-regime-boundary.sh:296-298 (a PR closed unmerged without an anchored reset record)

## Threat table, closed rows → tests

- Orchestrator edits `.orchestration`: `tests/unit/test_regime_counters.py::RegimeCountersTest::test_a_forged_acceptance_record_changes_no_count`.
- Anchor row (boundary cases in `tests/unit/test_check_regime_boundary.py`, the declared module, as the task says):
  - `RegimeBoundaryCountsTest::test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged`;
  - `…::test_a_reset_record_silences_only_when_another_identity_accepted_its_design`;
  - `…::test_a_waiver_line_silences_nothing`;
  - the counters half `tests/unit/test_regime_counters.py::RegimeCountersTest::test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity`.
- Unrelated accepted design (new): `tests/unit/test_check_regime_boundary.py::RegimeBoundaryCountsTest::test_a_reset_record_naming_an_unrelated_accepted_design_anchors_nothing`.
- 20-row truncation: `tests/unit/test_regime_counters.py::RegimeCountersTest::test_a_600_row_history_counts_fully_through_the_storage_facade` (store guard: `…::test_a_store_at_another_schema_revision_is_unreadable`).
- Extra RESULTs or PONGs, first-token status and verdict: `tests/unit/test_regime_counters.py::RegimeCountersTest::test_every_result_counts_as_a_revise_whatever_its_status` and `…::test_a_status_in_free_text_counts_nothing`.
- Bot heads: `tests/unit/test_regime_counters.py::RegimeCountersTest::test_v0_fixture_counts_bot_heads_after_the_first_result_head`, `…::test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head`, `…::test_bot_heads_are_unknown_when_gh_fails`, `…::test_bot_heads_are_unknown_without_a_first_result_head`, `…::test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id`, `…::test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit`, `…::test_only_p0_and_p1_heads_after_the_first_result_head_count`, `…::test_bot_heads_read_every_page_through_gh_api`.
- PR-less task: `tests/unit/test_check_regime_boundary.py::RegimeBoundaryCountsTest::test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr` and `tests/unit/test_regime_counters.py::RegimeCountersTest::test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one`.
- Test seams: `tests/unit/test_regime_counters.py::RegimeCountersTest::test_every_line_names_its_source` and `…::test_the_boundary_check_never_passes_a_test_seam`.
- Fixture budget: no test, measured by the pasted numstat (931 at `3ea405c8`, 944 at `e87a52fc`).
- Mutation checks at the final head: 41 rules removed in turn, 41 killed (validation file). Two first-pass survivors were fixed. One was a stale mutation still written with the deleted `has()`; jq's builtin `has` checks object keys, so it did nothing. The other was the hash guard, which the new `reset_of` check had shadowed; the added hash case above makes it load-bearing again.

## Live state and consequences

- `make check-regime-boundary` at the final head lists, for INV-6: T120 `amendments 7`, both T124 `waiver-unanchored` lines, `dotfiles-T128-process-rules-a01 bot_p1_heads 6`, `dotfiles-T128-process-rules-redesign-a02 revises 2`, and V0 `bot_p1_heads 6`. It exits 1. The two process-rules lines are tasks in flight elsewhere.
- Live replays are unchanged: V0 `--pr 317` gives first head adcf783b and 6 heads; T119 gives 10/9/8/6/5 and 4 heads. `--history-only` takes 0.38 s.
- The boundary probe now runs one `uv run --offline` per reset record whose hash matches its redesign file (three today). The online fallback needs pypi, which a sandbox blocks; there it fails closed (no anchor).

## Bot and CI

- CI on `3ea405c8`: 14 of 14 pass (validation file).
- Bot wait on `3ea405c8`: `bot: none` after the 15-minute bounded wait (07:23Z–07:38Z, reviews by `commit_id`, top-level comments by `original_commit_id`). Codex's 👍 on the PR moved to 07:16:07Z, after the 07:12:41Z push of `3ea405c8`; per step 15 a 👍 is not evidence of a review. bot_rounds=0 in a02 (no P0 or P1 finding); there are no open threads, since the orchestrator resolved every a01 thread.

## Other

- plan-mode-used: no. Understand-Anything hook: not seen.
- memory add: `uv run --offline --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T128 A3 a02 (…)"` from the main checkout → id `4d1c7263-d92a-4575-8277-51477355cc09` (command and output in the validation file).
- cost: n/a.

## Amendment 1 (TASK amendment=1, 09:41:42Z; task.md sha256 `a161f7e7…`; boundary PR 321, design `4520b8f0`, merged 09:40Z)

- `f10acc9a` recommits the task.md copy byte-identical at the new hash. `e87a52fc` is the content commit for the two rules and their tests. `gh pr update-branch` was not run, as instructed.
- **The reset accept is bound to `redesign_source`.** The accepting AGMSG-RESULT's `task_id` (its first token) must equal the reset record's `redesign_source:`, the review-seat task that produced the successor. The boundary probe passes it as `regime-counters.sh --reset-source <id>`; without a source nothing is accepted, not even a RESULT without a `task_id` (scripts/regime-counters.sh:117, scripts/check-regime-boundary.sh:253, :260). The `reset:` line now prints `redesign_source=`. The boundary's own `-n source` guard was deleted as redundant with the counter's: its mutation survived.
  - Tests: an unrelated review task's accept of the same hash (`T7-review`), and a record without `redesign_source:`, in `test_a_reset_record_silences_only_when_another_identity_accepted_its_design`. The counters half is `test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity`, which covers another task id's accept and the task_id-less accept with no source.
- **`pr=none` is bound to review and design task files.** `pr=none` silences only a task whose file has format-2 front matter with `kind: review` or `kind: design`. It is read by the same PyYAML helper, now `front_matter_says <file> reset_of <id> | pr_less` (scripts/check-regime-boundary.sh:216-241, :284-285).
  - Tests in `test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr`: a review task with `pr=none` is silenced. These are not: a code task (`kind: code`) whose RESULTs omit `pr=`, a file without front matter, `kind: review` without `format: 2`, a task whose RESULT names a PR, and a RESULT carrying `pr=none`.
- **Live state** (validation file): every anchor holds under the stricter rules. a01 is silenced through `redesign_source: dotfiles-T128-regime-counters-redesign-a01`. Both T124 records show only `waiver-unanchored`, anchored through `redesign_source: dotfiles-T128-design-review-a01` and design `4520b8f0`. No PR-less review task appears, since they all carry `format: 2` and `kind: review`. The INV-6 lines are T120 `amendments 7`, the two T124 waivers and V0 `bot_p1_heads 6`; the probe exits 1. The replays are unchanged: V0 6 heads after adcf783b; T119 10/9/8/6/5 and 4 heads; `--history-only` 0.38 s.
- `tests/` adds **944** lines. Mutation checks: 48 rules removed in turn, 48 killed. Three earlier mutations were retargeted at the renamed helper (`front_matter_says`) and restructured lines. 33 named tests and the 16 `regime_boundary` tests pass.
- CI on `e87a52fc`: 14 of 14 pass. Bot wait on `e87a52fc`: `bot: none` after the 15-minute bounded wait. The host slept during it (its end stamp reads 10:51:45Z), and the listing re-run on 2026-10-11 after 21:37Z still shows no Bot review or top-level comment on `e87a52fc`. Codex's 👍 on the PR is at 09:52:27Z, after the 09:48:35Z push; per step 15 a 👍 is not evidence of a review. bot_rounds=0 (no P0 or P1 finding in a02), and there are no open threads. The RESULT was delayed by the ~11-hour host sleep, as the orchestrator's 21:37Z PING notes.
- memory add (amendment 1) → id `e661abcf-e710-4294-a3ce-c5ff92c18718` (command and output in the validation file).
