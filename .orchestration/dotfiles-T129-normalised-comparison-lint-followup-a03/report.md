---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a03
seat: claude-standard-dot-a008
branch: lint/normalised-comparisons-followup-a01
pr: 415
reset_of: dotfiles-T129-normalised-comparison-lint-followup-a01
previous_head: c0eb536cd33b53084ae86d17ec66e82b476f3092
base: b22a5580
copy_commit: 088f377e
test_commit: 6db2187c
fix_commit: 4bb6092d
review_commit: 77bb5753
code_head: 77bb5753
task_sha256: 8356dfb5cd99223b1bbdda0eb3cc4fe5ba485f69006b81ebc2446ec034a4e5ce
---

# Report: dotfiles-T129-normalised-comparison-lint-followup-a03 (INV-6 reset of followup-a01, the changed-file lint gate)

- **Seat and task file:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. The AGMSG-TASK arrived at 2026-10-19T04:10:20Z with `task_sha256=8356dfb5…`. The dispatched file and the branch copy are byte-identical (validation §1). The task-consistency check passes (§1a).
- **Branch:** PR #415 continues on `lint/normalised-comparisons-followup-a01` from the chain's head `c0eb536c`, which merged main `b22a5580` into `7df91833`. origin/main is still `b22a5580`, so that is the merge-base (§2).
- **The C3 reset copy:** `088f377e` deletes the a01 task copy and adds the byte-identical a03 copy (§3). The first push carries it. Other inherited content is unchanged, apart from this task's implementation and records.

## Items 1 to 3

| Item | Change | Evidence |
|---|---|---|
| 1, `scripts/lint-comparisons.py` | **Scan:** the existing scan (the tracked files, or the explicit files) still supplies the hits and stale rows. **Severity, `--changed <path>...`:** an unbaselined hit or a stale row in a changed file is printed and exits 1. In an unchanged file it is printed as `warning: …`, counted, and closed by `warning: <h> unbaselined hit(s) and <s> stale row(s) in unchanged files`; a run with only warnings exits 0. **`--all`:** prints every hit, baseline-matched ones with ` (baseline)`, and every stale row, and exits 0. `--changed` and `--all` are mutually exclusive. **No mode flag:** the changed set is `git diff --name-only --no-renames -z --no-ext-diff --no-textconv origin/main...HEAD` (a rename changes both paths, as in test.yaml's decide step), and an empty set stays empty. **Isolated git:** that diff and the tracked-file scan run through one helper per plan 024 §5.14 item 2. It runs under `env -i` with only `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. The binary is git from the system directories (`os.defpath`), never the inherited PATH, run by its absolute realpath with an absolute `-C`, the six `-c` settings, NUL-delimited output and `check=True`. A missing git exits with a message. **Unchanged:** the rule table, `--list-rules`, the marker, the LIMIT line, duplicate consumption and the inherited fixes. | §5 red, §6 green, §7 the checkout lint, §8 `--all`, §9 rules unchanged |
| 2, the baseline | Unchanged since `c0eb536c`, with no `regime-ci.py` row (§9). The five hits in the unchanged `scripts/orchestrator/regime-ci.py`, at lines 65 (R6) and 71, 72, 90 and 246 (R4), are warnings in this PR's gate (§7). | §7, §9 |
| 3, the tests | The checkout test `test_the_tracked_tree_is_clean_against_the_baseline` becomes `test_the_changed_files_are_clean_against_the_baseline`. It computes the changed set itself with the same isolated git, runs the lint with no flag, requires exit 0 with an empty stderr, allows only `warning:` lines, and finds none naming a changed file. The four fixture tests are written first: `test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning`, `test_a_hit_in_a_changed_file_fails`, `test_a_stale_row_for_a_changed_file_fails` and `test_a_stale_row_for_an_unchanged_file_warns`. Each also asserts that `--all` exits 0 and prints its hit or stale row; the last one also checks a baseline-matched hit. The other fixture calls pass `--changed <fixture>` beside their explicit scan file, so every rule, normaliser, marker, exact-row and duplicate assertion keeps its meaning. | §5: the old checkout lint exits 1 on `regime-ci.py`, and the five tests fail at `c0eb536c`; the four fixture tests reject `--changed` and `--all` as unrecognised. §6: 14 of 14 green at HEAD: the 13, the three inherited selectors among them, and the review round's no-flag test. |

## Check (§6 to §11)

- **Unit tests:** `uv run python -m unittest tests/unit/test_lint_comparisons.py -v` exits 0, 14 tests (§6).
- **Ruff:** `ruff check scripts/lint-comparisons.py` exits 0 (§10).
- **The lint, no flag:** `uv run --no-project python -I scripts/lint-comparisons.py` exits 0 and prints the five `regime-ci.py` warnings with their count (§7).
- **The lint, `--all`:** exits 0 and prints 93 baseline-matched hits, the five unbaselined ones and no stale row (§8).
- **`make format` exits 2, an inherited failure.** It flags the same 12 files at the merge-base `b22a5580` as at HEAD, with shfmt v3.14.1 (§10a): ten `.orchestration/tasks/*-input/*.sh` files, `executable_project-map-reload.sh` and `brew.bats`. None of them is this PR's. The two Python files pass `ruff format --check` (§10).
- **Caps, origin/main...HEAD with merge-base `b22a5580` (§11):**
  - outside `tests/` and `.orchestration/`, the baseline included: 320 of 400 (the script 227, the baseline 93);
  - `tests/`: 390 of 450.
  - The measurement at `c0eb536c` matches the task: 293 and 271 (§4).

## Worker review

The worker review is recorded in `dotfiles-T129-normalised-comparison-lint-followup-a03-worker-crit.json` and its receipt. There was one pre-push round, the task's limit, covering `c0eb536c..4bb6092d`. It returned `Verdict: correct`, with one P2, five P3 and an evidence note. The fix round is `77bb5753` and counts toward INV-6 (C-61).

- **P2, fixed:** nothing tested the no-flag changed-set lookup that CI runs, and four broken lookups passed. `test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails` runs a copy of the script in a temporary repository with a real `origin/main`, after an update-branch merge. The change's own hits and a renamed-away file's row fail, main's hit in an unchanged file warns, and a missing base fails closed. Five mutants are killed (§6a): an empty set, no `-z`, the range reversed, `check=False`, and rename detection kept.
- **P3, fixed:** `--no-renames`, the usage order, and the checkout test's exact path match.
- **P3, residual:** a manual run naming an absolute path is read as unchanged, since paths are as git prints them and no caller uses this form.
- **P3, residual:** the git isolation is untested. The task is `security: false`, and its threat row for the script is residual.

## CI and Bot

- **CI:** it runs on the commit that adds these records, which is the final head; its results are in the RESULT. The chain's head `c0eb536c` failed the four `test` jobs on the old tracked-tree test; that failure is §5's red.
- **Bot:** PR #415 was already ready for review, so no automatic Codex review is expected on a push. The bounded window and its outcome are in the RESULT. No `@codex review` comment is posted.

cost: n/a
