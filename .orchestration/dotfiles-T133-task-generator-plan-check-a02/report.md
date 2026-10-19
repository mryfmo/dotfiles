---
task_id: dotfiles-T133-task-generator-plan-check-a02
round: 1
reset_of: dotfiles-T133-task-generator-plan-check-a01
status: result
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c).

- Branch `tools/task-generator-plan-check-a01`, PR #417, continued from 9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab. Base `origin/main` is 3e41e36a, which 9da0ed3f already merges.
- Commits:
  - 6da92853: the task-copy swap. `git rm` of the a01 copy, and the byte-identical a02 copy (sha256 `a3ab8ea6addda207fa9a9ff5d96921e080dab7a1025117f33cbd087e6b805f98`).
  - eb20d063: the implementation and its tests.
  - 6e07d291: the one correction round after the worker's pre-push review. It is the code head.
  - The evidence commit is last.
- INV-6 for a02: amendments=0, questions=0, revises=0. The a01 history, its acceptance records and its counters stay as recorded, including the C14 revise, which counts as the second amendment in substance (item 7).
- The worker's pre-push review: one round (below).

## What changed

### `scripts/orchestrator/task-from-plan.py` (items 1, 5, 6, 12 to 15)

- **Bundled template (items 1, 5):** `scripts/orchestrator/task-template.md`, beside the generator, supplies:
  - the ten control rows: the task copy, the evidence records, task metadata, metadata separators, in-process effects, workflow and interpreter or environment inputs, new or renamed scripts, and the three orchestrator effects, with `<task_id>` replaced;
  - the default Check (`make unit-test`, `make format`);
  - the full Completion paragraph, with `<task_id>-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/<task_id>/task.md>`.

  No file under `.orchestration/tasks/` is read. The sibling-task Check lookup, the row-template task and the Completion-record file are gone.
- **Clean-plan gate (item 6):** before anything runs or is written, `git status --porcelain=v1 --untracked-files=all -- ':(glob).orchestration/plans/024-*'` must print nothing and exit 0. Otherwise the generator exits with `task-from-plan: refused: the plan group has uncommitted changes; commit them first:` and the status lines. Every plan file is read with `git show <HEAD>:<path>`, so the executed command text is the committed text. The revision is named in the task's opening line (`read from the plan group at <sha>`).
- **Wave selection (item 12):** the seat's cell, or the whole row without `--seat`, must hold the todo id as a whole token, `(?<![\w-])P1-1(?![\w-])`. `P1-10`, `P1-11` and `P1-1a` never match `P1-1`.
- **Scopes (item 13):** a backticked first word with `/`, inside the checkout (the checker's `confined`), not starting with `-` or `~`, is proposed:
  - a literal has a file extension or exists;
  - a glob stays as written.

  Each executed or applied file a glob matches (`git ls-files :(glob)…`, the checker's own `applied()`, outside `tests/fixtures/`) gets a concrete row, `<file> (matched by <glob>)`. A match that is itself an allowed entry keeps only its own row, so no row names two entries (C7b). `git grep -l -F -e <name>` provenance stays in Files as `# from:`.
- **Program items (item 14):** an item runs from its `**(<n>) ` line to the next `**(<m>) ` line or the end of the file, so blank lines, fenced blocks and later paragraphs stay inside it.
- **Commands by form (item 15):** a span is a command when:
  - its first word is a lowercase name, a `/` or `./` path, or a `.sh` or `.py` path;
  - it holds no `<placeholder>`.

  Execution decides the rest, with stdin from `/dev/null` (the checker's `rerun`): an absent executable stays a premise, `verify: \`cmd\` exits 127`. Redirects stay. A lone word counts only when PATH holds it, since a lone `residual` or `kind` is prose, and a lone path is a scope. `make …` spans go to the Check; the others are premises, run through the checker's `rerun`. A gh, curl or URL command is a `verify:` not-run premise with an empty output.
- **Check:** each command, the template's plus the items' `make` spans, runs once in a detached scratch worktree of `origin/main`. It is pasted as ``- `cmd`: exit N on origin/main <rev12>``, followed by a fenced tail of its last 20 output lines. The worktree is removed with `git worktree remove --force` and its temporary parent deleted.
- The generator still runs the checker on the written file with `--premises-sha` of those bytes, the generator's own text whose premises it has just run.

### `scripts/orchestrator/task-consistency-check.py` (items 2, 7 to 10, 19, 20)

- **C14 (items 7, 8):** the sha gate is kept, so premises run only for the file whose sha256 `--premises-sha` names. Without it the file gets `<file>: warning: C14: not run (no trusted sha)` on stderr. Absent tools are `<file>: warning: C14: tool absent …`, and skipped network premises `<file>: note: C14 skipped network premise …`. Stdout, and with it the finding format, is unchanged.
- **C15 (item 9):** the assignment comes from the design on `origin/main`, for tasks with or without `invariants`:
  - `implementing_tasks` as a map from task to ids: each assigned id the task lacks is `C15 invariant <id> that <design> assigns to <task> is missing`, and each id it carries but was not assigned is `C15 invariant <id> is not one <design> assigns to <task>`;
  - the list form (T124, T126) names no ids per task and so assigns none;
  - the sentences of the ids in force must be byte-equal, as before;
  - `C15 design <design> is not on origin/main` is reported in two cases. Existence comes from C8's `git cat-file -e origin/main:<design>` probe.
    - For a task that carries invariants, when origin/main cannot give the design.
    - For any task, when the path names no design on origin/main or in the checkout, so a mistyped path never skips the check.

    The one exemption is a design that exists only in this checkout, for a task without invariants: it assigns nothing yet. See "Observations".
  - A design without front matter assigns nothing instead of raising.
- **C12 (items 10, 19):** each glob entry's `git ls-files :(glob)` matches decide, whatever the glob spells. An executed or applied match (`*.sh *.py *.yaml *.yml *.json *.toml`, or a path under `home/`, `scripts/`, `.githooks/` or `.github/`) needs a row naming it. `tests/fixtures/` and the task's own evidence directory stay exempt.
- **C10 and C6 (item 20):**
  - C10 passes each backticked literal as `git grep -qF -e <literal>`, so `--open-files-in-pager=<cmd>` is searched for and nothing runs;
  - a rule sentence's script path outside `--root` is `C10 rule sentence names <path>, a path outside the checkout`;
  - C6 reads a design path only inside the checkout, and `C6 design path <path> is outside the checkout` otherwise. C15 reuses the same confined path.

### `scripts/orchestrator/plan-check.py` (items 3, 11, 16 to 18)

- **F2 (item 11):** each task's allowed list becomes its literals plus the files each glob matches in the tree (`glob.glob(…, recursive=True, include_hidden=True)`). Two lists overlap on:
  - a shared path;
  - a path inside the other's directory;
  - a literal the other's glob matches (`fnmatchcase`), for a file not yet in the tree.

  Two glob spellings are never compared. The finding names the first shared path.
- **Acceptance drift (item 16):** a progress row's task takes its latest `AGMSG-ACCEPTANCE v1 … task_id=<task> … status=<[\w-]+>` event.
  - Each event on a line is read up to the next one, so another task's event never lends its status.
  - Events are ordered by the last ISO timestamp before the event on its line. An untimed event carries the latest timestamp above it, then position decides.
  - Records without timestamps keep textual order.
- **PR drift (item 17):** every sha or state word that starts within 40 characters after a `#<pr>`, before the next `#`, is compared on its own, deduplicated per line.
- **Invariants (item 18):** `ANTHROPIC_OAUTH_TOKEN=` followed by a non-empty `"…"`, `'…'` or bare value is a finding. `""` and `''` are not. The finding never carries the value.

## Item 19: ownership

The audit of 9da0ed3 (P2, finding 15) assigned the C12 remedy to the advisory owner `dotfiles-T133-task-generator-plan-check-followup-a01`. Item 10 of this task now owns it:
- selector: `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling`;
- fix: eb20d063.

The orchestrator records the corrected ownership and withdraws the remedy from the follow-up task. Findings 1 to 14 of that audit are likewise fixed here under items 5 to 18.

## Tests

New, each red against 9da0ed3f with this branch's test source and green on the final head (validation.md):

| Item | Test |
| --- | --- |
| 5 | `tests/unit/test_task_from_plan.py::test_generator_uses_the_bundled_template_without_task_records` |
| 6 | `tests/unit/test_task_from_plan.py::test_generator_refuses_dirty_plan_commands_before_execution` |
| 12 | `tests/unit/test_task_from_plan.py::test_wave_selection_matches_whole_todo_ids` |
| 13 | `tests/unit/test_task_from_plan.py::test_generator_preserves_wildcard_scopes_and_their_threat_rows` |
| 14 | `tests/unit/test_task_from_plan.py::test_program_item_continues_until_the_next_numbered_heading` |
| 15 | `tests/unit/test_task_from_plan.py::test_generator_retains_unavailable_single_word_and_redirecting_commands` |
| 11 | `tests/unit/test_plan_check.py::test_f2_detects_intersecting_globs_through_concrete_tree_matches` |
| 16 | `tests/unit/test_plan_check.py::test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task` |
| 17 | `tests/unit/test_plan_check.py::test_drift_checks_every_sha_and_state_for_each_pr_occurrence` |
| 18 | `tests/unit/test_plan_check.py::test_invariants_reject_nonempty_quoted_oauth_token_assignments` |
| 8 | `tests/unit/test_task_consistency_c11_c15.py::test_c14_without_a_trusted_sha_reports_an_explicit_warning` |
| 9 | `tests/unit/test_task_consistency_c11_c15.py::test_c15_requires_the_design_assigned_invariant_id_set` |
| 10, 19 | `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling` |
| 20 | `tests/unit/test_task_consistency_c11_c15.py::test_c10_never_passes_a_literal_as_a_git_grep_option` |
| 20 | `tests/unit/test_task_consistency_c11_c15.py::test_c6_confines_design_paths_to_the_checkout` |

Retained, item 7: `tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha`, red at ff4d25a8, the revision before the gate. Its no-sha expectation now carries item 8's `warning:` prefix.

Retained end-to-end tests (item 4), each changed only where the a02 behaviour changes:

- `test_task_from_plan.py::test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs` now expects:
  - the bundled control rows, with no `dotfiles-T133-result-precheck-a01` text;
  - the Check line ``- `make unit-test`: exit 0 on origin/main <rev12>``;
  - a failed premise claim starting `verify:` with `exits 3`.

  The fixture still commits the legacy task records the a01 generator needed. That way each new regression is red against 9da0ed3 for the reason it names, not for a missing file. The legacy rows' dispositions are at least 20 characters, so the a01 generator's output does not fail C11 first.
- `test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan`: the F2 glob subtest now names the concrete shared path, `share scripts/two.py`.
- `test_task_consistency_c11_c15.py::test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged`: the absent-tool expectation carries the `warning:` severity. Its subprocess calls carry explicit `check=` flags.
- `tests/unit/test_task_checkers.py` is unchanged by a02. It carries only amendment 1's two edits from a01, and its historical expected sets stand: C11 and C15 only on regime-counters and ci-skip.

## Real runs (validation.md)

- **The checker:** run with the code head 6e07d291 on the main checkout's 29 `dotfiles-T133-*.md` files, with `--root <main checkout>` (at 740772ef, after #416) and without a sha, it exits 0.
  - Stdout: 29 `OK`. C1 to C13, C15 and C7b found nothing.
  - Stderr: 20 `warning: C14: not run (no trusted sha)` lines, one per file with premises. C14 executed nothing and is recorded as not run, not as passed.
  - The run on eb20d063, before the correction, gave the same result over the 24 files that existed then.
- **`plan-check.py`:** run once against the main checkout, on eb20d063's code, it exits 1 with six violations. The correction round changed only `--drift`'s acceptance reading, which this flagless run does not use. They are the same six a01 reported, left for the orchestrator:
  - F3 (P1-13, P1-14);
  - F4 (P1-a);
  - three F6 citing `dotfiles-T131-claude-pinned-merge-gate-fix-a01`.

  No F2 overlap appears with concrete scopes.

## Observations for the orchestrator (no change made)

- **Dispatch wiring (item 8's owner):** `scripts/orchestrator/dispatch.sh:238` runs `task-consistency-check.py --root "${root}" "${tf}"` without `--premises-sha`. So C14 never runs at dispatch, and its `2>&1` capture prints the warning only when the check fails. The needed change is `--premises-sha "$(value_of task_sha256)"` plus forwarding the stderr warning on success. Both belong to the P1-5 to P1-6 dispatch lineage, as item 8 states.
- **C15 and a missing design:** the item 2 text says a missing named design produces a finding. The checker reports it in every case but one: a design that exists only in this checkout, for a task without invariants.
  - That exemption exists because `tests/unit/test_task_checkers.py`'s fixtures are such tasks: their stub `git` answers `cat-file -e` and exits 99 on `show`, or the design exists only in the fixture root. That module may carry only amendment 1's two edits.
  - The unconditional finding turned its C4, C9, complete-file and historical tests red.
  - A mistyped path, absent everywhere, is a finding, which was the review's P2.

  If the orchestrator wants the strict reading for in-flight designs too, the fixture module needs an amendment.
- **Lone-word premises:** the real plan quotes field names such as `head` and `security` as lone backticked words. Item 15's lone-word rule runs them as draft premises. With stdin closed, `head` prints nothing and `security` prints its usage with `verify: … exits 2`. The orchestrator deletes such rows from the generated draft, which stays for editing.
- **The plan group is untracked:** `.orchestration/plans/024-*` exists only untracked in the main checkout, so item 6's gate refuses to generate there until the group is committed. That is intended.
- **Network-free does not mean harmless:** the generator, and C14 at dispatch, run every recognised command in a program item; only gh, curl and URL commands are skipped. A program item quoting a write such as `git push …` would run in the orchestrator's sandbox. That is item 6's stated contract for the orchestrator's own committed text, but the skip list is narrow.

[memory:decision] T133 P1-12 a02: task-from-plan.py reads only scripts/orchestrator/task-template.md (no .orchestration/tasks/), refuses a dirty .orchestration/plans/024-* group before running or writing, reads the plan at HEAD, and recognises commands by form; plan-check F2 and checker C12 decide on concrete tree matches; C14 without a trusted sha is a stderr warning; C15 compares the design-assigned invariant id set; C10 passes literals after git grep -e and C6/C10 paths stay in the checkout.

## Pre-push review

One round, on eb20d063, by a fresh read-only subagent: `Verdict: incorrect`, two P2 and four P3, each reproduced. The record and its receipt are `dotfiles-T133-task-generator-plan-check-a02-worker-crit.json` and `…-worker-review-receipt.md` here. All six are fixed in the one correction round, 6e07d291:

- **P2, `plan-check.py` `latest()`:** another task's event on the same line lent its status, timed lines outranked every untimed one, and a trailing backtick stayed in the status. It now reads each event separately, carries timestamps, and captures `[\w-]+`.
  - Regression: `test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task`, red against eb20d063 (`accepted != withdrawn`` `).
- **P2, C15 missing design:** a mistyped path skipped the check. Existence now comes from `cat-file -e`, and a path absent everywhere is a finding for any task.
  - Regression: `test_c15_requires_the_design_assigned_invariant_id_set`, case `a mistyped design`, red against eb20d063.
- **P3, `rerun` stdin:** a lone `head` premise waited on the caller. It now gets `stdin=subprocess.DEVNULL`.
- **P3, the generator's output failed C7b:** a glob over a literal entry gave a second row. It is fixed, and `test_generator_preserves_wildcard_scopes_and_their_threat_rows` adds `scripts/*.sh` over the literal `scripts/demo.sh`; red against eb20d063.
- **P3, C15 on a design without front matter:** it is parsed only when it opens with `---`.
- **P3, test gaps:**
  - item 17 now has a repeated PR with several tokens per occurrence;
  - C12's own-directory exemption has a real tracked file.

  Both pass against eb20d063, because they fill gaps rather than show defects, and both are red against 9da0ed3.

A first attempt at the review read worker-c directly and was stopped, before reporting anything, when the orchestrator's #411 revise needed the worktree (sandbox.md). It is not counted as a round.

## Feedback dispositions

The Bot's review of a01 (5562936729, on 35c66022) left three threads on PR #417. Each gets its root-cause disposition; the orchestrator replies and resolves:

- **4306960622 [P1] Sandbox premise commands before executing them** (`task-consistency-check.py:75`): fixed:538e60bd.
  - The checker executes premises only for the file whose sha256 `--premises-sha` names, the orchestrator's dispatched text. A PR-controlled copy at acceptance has no trusted sha, so nothing runs; it gets item 8's warning.
  - a02 keeps this gate (item 7; red at ff4d25a8, green here) and closes stdin in 6e07d291. The generator runs only committed plan text (item 6).
- **4306960626 [P1] Bundle the required task template** (`task-from-plan.py:131`): fixed:eb20d063.
  - The template is `scripts/orchestrator/task-template.md`, and nothing under `.orchestration/tasks/` is read (item 5).
  - Regression: `test_generator_uses_the_bundled_template_without_task_records`, which deletes `.orchestration/tasks/` from the fixture.
- **4306960630 [P2] Resolve globs before checking wave overlaps** (`plan-check.py:89`): fixed:eb20d063. F2 compares concrete tree matches, plus literals a glob matches (item 11).
  - The Bot's case, `scripts/*.py` against a literal `scripts/two.py`, is the retained F2 glob subtest.
  - Two intersecting globs are `test_f2_detects_intersecting_globs_through_concrete_tree_matches`.

The task-level audit of 9da0ed3 (three P1, twelve P2) is dispositioned item by item above: items 5 to 19, plus item 20's PR #418 review.

This push: no `@codex review` is posted. CI on the final head and the 15-minute Bot window are in the RESULT line.

## Amendment 1: the CI-repair round

The chain update-branched PR #417 onto main b22a5580 (63b6acae). The regime verifier from PR #418 now runs this task's checker on the fixtures in `tests/unit/test_regime_ci.py`. Their threat rows carried a bare `disposition: residual`, which C13 refuses (and C11, as a payload under 20 characters). Three regime tests failed in CI and five locally (validation.md).

Commit eb0b1c06 gives each of the five fixture rows `'residual: the compensating control of this fixture'` and copies amendment 1's task text. No expected output and no production file changes.

- The regime tests are red on 63b6acae.
- 101 tests across the regime, task and orchestrator-tool modules are green on eb0b1c06.
- Caps against the new merge base: 659 of 700 outside `tests/` and 673 of 800 under `tests/`.

This is one CI-repair round under C-61. The worker's pre-push review round of a02 is unchanged.
