# Report: dotfiles-T128-regime-counters-a01 (plan 006 Phase A3, INV-6 counting half)

- Worker: `claude-standard-dot-a004` (Claude seat, `.claude/worktrees/worker-c`; the parked `feat/main-tests` branch left untouched).
- Branch `feat/regime-counters` from `origin/main@b896d9bc`; PR #319 (draft opened 04:26:47Z, 9.5 min after the TASK; ready 05:02:56Z); final head `72764f05ea0091b9e41203829cf9ff8e0e759924` (Amendment 1 round; the first RESULT was at `324652e0`).
- Commits: `f56f46a0` task.md copy (byte-identical, sha256 `69fee495…`), `0749a556` scripts, `9819ec3e` tests and fixtures, `ff41da6e` plain task ids and the stdin of the id loop, `e2dd97dc` shfmt (CI), `324652e0` Bot round 1, `f372d4ba` task.md recommit at Amendment 1 (sha256 `d9a44b7e…`), `33d8307b` Amendment 1 (`pr=none`), `72764f05` the Codex Bot login filter (final head).
- Evidence layout follows V0's precedent on its own branch (`git ls-tree feat/main-tests .orchestration/dotfiles-T128-v0-main-tests-a01/` holds only `task.md` and `revise.yaml`): the branch carries the task.md copy; the report, validation, sandbox, learning and autoskill files are at the TASK's expected main-checkout paths.

## What was built

1. `scripts/regime-counters.sh` (new, 149 lines, shdoc header, shellcheck and shfmt clean). `<task id> [--team] [--pr] [--history-only] [--reset-hash <sha256>] [--history-file <tsv>] [--github-file <json>] | --list-tasks`. Output line exactly as the task specifies, then `S2:` lines, then `S1:` lines; every line ends in `source=live|fixture`. Two lines are appended after the S1 lines: `detail:` (PR: digits, `none` when no RESULT carries `pr=`, `invalid` for another value; TASK senders, every counted message id, every counted Bot head; threat row 5 "every counted message id printed") and, with `--reset-hash`, `reset:`.
   - `withdrawn=` is the count of `AGMSG-ACCEPTANCE … status=withdrawn` for the task, informational; it changes no count (the task's output line names it but does not define it).
   - Two flags beyond the task's list, both used only by the boundary probe: `--list-tasks` (one history read gives the TASK'd ids: 20 of 335 task files; one counters call per file would cost ~0.2 s × 335) and `--reset-hash` (the anchor needs history, which only the counters read).
2. `scripts/check-regime-boundary.sh`: one probe appended before the print loop; the existing probes are unchanged. Skips without the counters script beside it or a readable store (the herdr scratch-worktree tests copy the boundary script alone: all 16 `regime_boundary` tests pass).
3. Tests: `tests/unit/test_regime_counters.py` (23), `tests/unit/test_check_regime_boundary.py` (8); fixtures under `tests/fixtures/regime-counters/`, masked with `--mask-secrets` (2 home paths in the V0 TSV).

## invariant lines

Line numbers at the final head `72764f05`.

- invariant: INV-6 → scripts/regime-counters.sh:48 (thresholds: INV-6's constant 2 for every count)
- invariant: INV-6 → scripts/regime-counters.sh:85 (history through `storage_history`, the whole team, no `--limit`; schema guard :83)
- invariant: INV-6 → scripts/regime-counters.sh:103 (a message belongs to the task of its first `task_id=` token)
- invariant: INV-6 → scripts/regime-counters.sh:141 (amendments = TASKs − 1; revises = RESULTs − 1, no status excluded)
- invariant: INV-6 → scripts/regime-counters.sh:112 (questions = `PONG status=question`)
- invariant: INV-6 → scripts/regime-counters.sh:114 (first RESULT's `head=`)
- invariant: INV-6 → scripts/regime-counters.sh:115 (the task's PR: digits, `none` when no RESULT carries `pr=`, `invalid` otherwise; only digits are fetched, :126)
- invariant: INV-6 → scripts/regime-counters.sh:132-137 (Codex Bot P0/P1 heads after the first RESULT head in PR commit order; `unknown`, never 0)
- invariant: INV-6 → scripts/regime-counters.sh:92 (`gh api --paginate`, every page)
- invariant: INV-6 → scripts/regime-counters.sh:117 (design accepted by an identity other than the task's TASK senders)
- invariant: INV-6 → scripts/check-regime-boundary.sh:250 (accepted acceptance record anchored on the task's PR merged on GitHub; record `pr=` parsed at :245)
- invariant: INV-6 → scripts/check-regime-boundary.sh:252 (Amendment 1: `pr=none` silences only a task whose RESULTs carry no `pr=`)
- invariant: INV-6 → scripts/check-regime-boundary.sh:226-228, 248-249 (reset record anchored on its redesign task file's hash and a foreign accept)
- invariant: INV-6 → scripts/check-regime-boundary.sh:260-262 (a `DESIGN_RESET_WAIVED_BY=` line silences nothing, reported `waiver-unanchored`)
- invariant: INV-6 → scripts/check-regime-boundary.sh:263-265 ("reports a closed-unmerged PR whose task has no reset record": INV-6's clause, implemented although the build list omits it; it needs the same `pulls/<n>` read as the merged anchor)

## Threat table, closed rows → tests

- Row 1 (orchestrator edits `.orchestration`): `tests/unit/test_regime_counters.py::RegimeCountersTest::test_a_forged_acceptance_record_changes_no_count`.
- Row 2 (anchor row; per the task, the boundary probe's cases are in `test_check_regime_boundary.py`, the declared module of the boundary script):
  - forged accepted record with an unmerged PR: `tests/unit/test_check_regime_boundary.py::RegimeBoundaryCountsTest::test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged` (also: merged PR but the record names another PR, the PR only inline as "PR #5", a PENDING decision);
  - reset record whose hash has no foreign RESULT: `tests/unit/test_check_regime_boundary.py::RegimeBoundaryCountsTest::test_a_reset_record_silences_only_when_another_identity_accepted_its_design` (author-only accept; record naming another or a missing redesign task; record without a hash) and the counters half `tests/unit/test_regime_counters.py::RegimeCountersTest::test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity`;
  - waiver line in an acceptance record: `tests/unit/test_check_regime_boundary.py::RegimeBoundaryCountsTest::test_a_waiver_line_silences_nothing`.
- Row 4 (20-row truncation): `tests/unit/test_regime_counters.py::RegimeCountersTest::test_a_600_row_history_counts_fully_through_the_storage_facade` (the fake facade fails on a `--limit`); store guard `…::test_a_store_at_another_schema_revision_is_unreadable`.
- Row 5 (extra RESULTs or PONGs): `tests/unit/test_regime_counters.py::RegimeCountersTest::test_every_result_counts_as_a_revise_whatever_its_status` (ready_for_review and blocked RESULTs; withdrawn and parked ACCEPTANCEs; PONG blocked; a later `task_id=` token; ids printed).
- Row 6 (Bot heads): recorded fixtures `…::test_v0_fixture_counts_bot_heads_after_the_first_result_head`, `…::test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head`; negatives `…::test_bot_heads_are_unknown_when_gh_fails`, `…::test_bot_heads_are_unknown_without_a_first_result_head`, `…::test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id`, `…::test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit`; ordering and badge `…::test_only_p0_and_p1_heads_after_the_first_result_head_count`; pagination `…::test_bot_heads_read_every_page_through_gh_api` (all in `tests/unit/test_regime_counters.py::RegimeCountersTest`).
- Row 7 (test seams): `tests/unit/test_regime_counters.py::RegimeCountersTest::test_every_line_names_its_source` and `…::test_the_boundary_check_never_passes_a_test_seam`.
- Row "a task without a pull request" (Amendment 1): `tests/unit/test_check_regime_boundary.py::RegimeBoundaryCountsTest::test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr` (a PR-less review task with `pr=none` is silenced; the same record on T1, whose RESULTs name PR 5, is not; a PENDING `pr=none` record is not; a RESULT carrying `pr=none` makes the record a forgery) and the counters half `tests/unit/test_regime_counters.py::RegimeCountersTest::test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one`.
- Every closed-row rule was mutated and its test failed (validation file, "mutation checks": 36 killed at the final head); three first-pass survivors were fixed (a test message that did not exercise the first-token rule; a redundant `-x` check, deleted; T9 below every count).

## Where the fixtures and premises disagree with the task text or baseline.md (tests follow the fixtures)

- [memory:decision] T119: `amendments=9`, not the premise's and baseline's 8. Ten TASKs; the ninth after the first is message `01a122a3-d648-7fb9-8355-13b5fb11d9c9` (2026-10-09T21:48:45Z, `note=task-file-repaired`, no `amendment=` token), which INV-6's sentence ("AGMSG-TASKs after the first") counts. The acceptance replay comparing against 8 will see 9. Codex P2 4240344214 raised the same point on task.md:24.
- [memory:decision] V0: `first_result_head=adcf783b` (the 01:42:31Z RESULT `01a128a0-…`), not premise 3's 32fe9a36 (that is the second RESULT's head, 02:19Z). Bot P0/P1 heads after it: 32fe9a36, 56ca6c69, de138f65, f6528bba, 2602f575, e314c502 = 6 (98f1d250 carries only a P2). Counting after 32fe9a36 would give 5.
- T118: `revises=9` (10 RESULTs), baseline 20 (ACCEPTANCE status=revise count); `amendments=1` (2 TASKs), baseline 7.
- T124 W1: `amendments=9`, baseline 8; `revises=1` (2 RESULTs), baseline 2; Bot heads after a11e3617: e6b30e96, 52bb69fc = 2. The baseline's "Bot P0/P1" column counts comments (T119 7, W1 31), INV-6 counts heads (T119 live: fd4ff82d, 2453b1c9, 70361875, 50759078 = 4, verified against `pulls/312/commits` order; 7903de38 precedes the first RESULT head 3cbcf388).
- S1: no class reaches three on PR 313 or PR 317 by the literal rule (first three words); the PING's hand-judged "same class" on PR 317 used different wording.
- Fixtures were exported through the storage facade (the script's own read) as `id at from to body` TSV, rows whose body contains `task_id=<id>`, not `history.sh --limit 2000` (its output is not TSV). PR fixtures keep the fields the script reads, each body cut to its title line.

## Consequences the orchestrator decides on

- At the first RESULT no record carried an anchor, and `make check-regime-boundary` listed T114, T118, T119, T120, T124 (four tasks), T128 design-review, task-review contracts and v1-v2, process-rules and V0. After the orchestrator added `pr=<n>`/`pr=none` lines and reset-record hashes in the main checkout, the live run at the final head lists only `dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7`, `waiver-unanchored` for both T124 reset records, and `dotfiles-T128-v0-main-tests-a01 S2: bot_p1_heads 6`, and still exits 1 (validation file). A reset record's `design_sha256:` must be the sha256 of its `redesign_task:` file.
- Review tasks were flagged by the literal rule, since each review round is an AGMSG-RESULT (`dotfiles-T128-design-review-a01` revises 26). With Amendment 1 a PR-less task is silenced by a `pr=none` accepted record.
- The probe makes about three `gh api` GET calls per counted task; a live run takes ~30 s. Inside a sandbox without gh TLS, Bot counts print `unknown` and the merged anchor fails closed.
- Row 3 (PR-authored script, tests and fixtures) stays the residual the task states; rows 8 (audits) and 9 (thresholds) as stated.

## Bot and CI

- CI on `324652e0` (the first RESULT's head): all 14 checks pass (validation file, `gh pr checks 319`). On `ff41da6e` the four test jobs failed at `shfmt` (CI runs `shfmt -i 4 -sr`; fixed in `e2dd97dc`). `public-bootstrap (ubuntu-24.04, client)` failed on a snap store HTTP 408 (network, not this change), and fail-fast cancelled the other two bootstrap jobs.
- Bot round 1, the Codex review of `ff41da6e` (review 5481983748, 05:07:46Z):
  - 4240344209 (P1, scripts/regime-counters.sh:117, "Bind reset approval to the named redesign task"): `fixed:324652e0`. Root cause: the hash a reset record names was not tied to the record's `redesign_task`. The Bot's suggested binding (the accepting RESULT's `task_id` must equal `redesign_task`) would never anchor a real reset: the accept of the T128 redesign is the review task's RESULT (`task_id=dotfiles-T128-design-review-a01`, `design_sha256=15957fbc…`), not the design task's. The fix: `design_sha256:` must equal the sha256 of `.orchestration/tasks/<redesign_task>.md`, so an accepted hash of another design anchors nothing (scripts/check-regime-boundary.sh:219-228). Tests: another, a missing, or no redesign task, all in `test_a_reset_record_silences_only_when_another_identity_accepted_its_design`.
  - 4240344212 (P2, scripts/check-regime-boundary.sh, "Report unanchored waivers outside the S2 branch"): `fixed:324652e0`. A `DESIGN_RESET_WAIVED_BY=` line is now reported for every counted task, with or without S2 lines or an anchor. Test: `test_a_waiver_line_silences_nothing`, which covers below every count, silenced by a merged PR, and a closed PR.
  - 4240344214 (P2, task.md:24, "Correct the T119 amendment baseline"): proposed `not-applicable: task.md is the byte-identical copy of the dispatched task file (sha256 69fee495…) and the worker cannot change it; the finding is right on substance, since INV-6's sentence gives 9 and the fixture test asserts 9; the orchestrator's acceptance replay should compare T119 against 9 (see "Where the fixtures and premises disagree")`.
  - 4240344216 (P2, task.md:17, "Persist the commit ID required by the invariant"): proposed `not-applicable: recording original_commit_id in scripts/pr-feedback.py is V3a's deliverable in the design (dotfiles-T128-regime-v3-a01.md: "V3a INV-6: scripts/pr-feedback.py (original_commit_id on review_comment items)") and pr-feedback.py is outside this task's allowed_files; threat row 6 has A3 read original_commit_id live with gh api; the counted heads are printed in the detail: line (bot_heads=), so an acceptance record can pin them`.
- Bot round 2, on `324652e0`, the first RESULT's head (diff head; `e2dd97dc` is the shfmt commit before it): `bot: none` after the 15-minute bounded wait (05:23Z–05:38Z, listing reviews by `commit_id` and top-level comments by `original_commit_id`). Codex left a 👍 reaction on the PR at 05:13:06Z, after both later pushes (05:07Z, 05:10Z); per step 15 a 👍 is not evidence of a review, so this is recorded as `bot: none`.
- The four round-1 threads were dispositioned and resolved by the orchestrator (Amendment 1).

## Amendment 1 round (TASK amendment=1, 05:54:36Z; task.md sha256 `d9a44b7e…`)

- `f372d4ba` recommits the task.md copy byte-identical at the new hash. `33d8307b` implements the added threat row. An accepted acceptance record with a `pr=none` line silences a task only when none of its RESULTs carries a `pr=` token. Any `pr=` token counts, so a RESULT saying `pr=none` makes the record a forgery: the counters print `pr=invalid` for a non-numeric token and fetch GitHub only for digits. All 36 `pr=` tokens on RESULTs in the store are numeric today.
- CI on `33d8307b`: 14 of 14 pass. The Codex review of `33d8307b` (review 5482116532, 06:03:56Z) left one finding:
  - 4240473132 (P2, scripts/regime-counters.sh:135, "Restrict counted reviews to the Codex bot"): `fixed:72764f05`. INV-6 names the Codex Bot, and the counters had accepted any GitHub App (`user.type == "Bot"`). Heads and S1 classes now count only `chatgpt-codex-connector[bot]`, the login of every Bot comment on PRs 313 and 317. Tests: another app's P0/P1 comments on post-RESULT heads and its titles are ignored in `test_only_p0_and_p1_heads_after_the_first_result_head_count` and `test_s1_candidates_are_bot_title_classes_seen_three_times`.
- CI on the final head `72764f05`: 14 of 14 pass. Bot wait on `72764f05`: `bot: none` after the 15-minute bounded wait (06:21Z–06:36Z). Codex's 👍 reaction on the PR moved to 06:14:11Z, after the 06:11:36Z push of `72764f05`; per step 15 a 👍 is not evidence of a review.
- bot_rounds=1. No P0 or P1 finding was raised after round 1; the round-2 finding was a P2. Unresolved threads: 4240473132 fixed:72764f05. No thread was resolved or replied to by the worker.

## Local test environment

`make unit-test` in this sandbox: 953 tests, the same 78 failures and errors on this branch and on `origin/main@b896d9bc` (a scratch worktree, removed with `git worktree remove`), none in the three named modules. The sandbox denies `~/.ssh/id_ed25519*` while the global git config signs commits, so every test that commits errors in setup; `GIT_CONFIG_GLOBAL=/dev/null` removes those. CI is the authority.

## Sandbox exits (through the permission gate)

`gh` (PR, CI, fixtures, live counts), `git push` (HTTPS with the gh credential helper and `GIT_CONFIG_GLOBAL=/dev/null`: the global `pushInsteadOf` rewrites to SSH, and no SSH key is readable), `make check-regime-boundary` and the live counter runs (gh), writing these artifacts into the main checkout, `memory add`, `agmsg-dispatch`. Details in the sandbox file.

## Other

- plan-mode-used: no. Understand-Anything hook: not seen.
- memory add: `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T128 A3 (PR 319, …)"` from the main checkout → id `1a2cbd75-7d8b-45dd-ab7a-21710a305caa` (first RESULT; its output is in the round-1 section of the validation file), and for Amendment 1 → id `6dda48a5-20ce-47b1-abef-01b8cabe5bf8` (full command and output in the validation file).
- cost: n/a (the runtime does not expose session cost to the worker).
