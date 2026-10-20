---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a04
seat: claude-standard-dot-a008
reset_of: dotfiles-T129-normalised-comparison-lint-followup-a02
pr: 432
branch: tools/lint-comparisons-followup-a02
anchor: e520a7fe4dd5f84acb46927927999998c188eb51
start_head: b24d3136b35e77efe647bdb6d487d9c76503d4c6
base: ba318e5369b14a79d6f515e87b685c9bcb30c12e
test_commit: 762682d7
fix_commits: eb6a58f0 c929569b
review_round_1_commit: d74204e6
code_head: d74204e6dd27a205e6d1bd1d83af704fed942f9b
records_commits: 09a51c50 (first push) and the validation commit after it (records only)
task_sha256: e7019c3c0dffc989bae6027d7b0d045d409a5d8ca3eb391bfe19fd08ce8afa39
correction_rounds: 1 of 2 (the pre-push worker review)
---

# Report: dotfiles-T129-normalised-comparison-lint-followup-a04 (the INV-6 reset of followup-a02, shell syntax from shfmt's AST)

- **Seat and task:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`.
  - The TASK (`e58d51b1…`) arrived at 2026-10-20T00:04:25Z.
  - The probe of shfmt's bash dialect over the tracked tree refused 14 of 165 shell targets (validation §3), so this seat sent a question PONG at 00:19Z with three default proposals.
  - Amendment 1 (`e7019c3c…`) at 00:21:47Z adopted them and added the pinned mise fallback.
  - The branch copy of the task is byte-identical to the dispatched file (validation §1).
- **Branch:** PR #432's `tools/lint-comparisons-followup-a02` continued from `b24d3136`. That head is the anchor plus the chain's main merge `ba318e53`, which added one baseline row and changed no lint or test code (validation §2). The base `origin/main` is `ba318e53`, equal to the merge-base.
- **Callers read before editing:**
  - `tests/unit/test_lint_comparisons.py`;
  - `tests/unit/test_update_agent_assets.py:329`, which runs `--all` on the updater script and passes (validation §7).
  - No workflow, Makefile target or other script runs the lint.

## The design as built (`scripts/lint-comparisons.py`)

- **The shell reader:** shell is read only from `shfmt -ln bash|zsh --tojson`, with the file contents passed as data.
  - **Removed:** `comments()` (the quote-state scanner and heredoc regex), the continuation joiner, `words()` (the shlex fallback), `programs()` with `JQ_QUOTE`/`JQ_ARG` (the regex jq locator), and `PS`/`WORD`/`PGREP`/`GREP`.
  - **Python:** still read by `ast` and `tokenize`, unchanged.
- **Choosing shfmt (amendment 1):** `shfmt` on PATH, else `mise x shfmt@3.14.1 -- shfmt`, each probed with `--version`. When neither runs, the lint exits nonzero with `lint-comparisons: shfmt missing`.
- **Refusals:**
  - A parse failure exits with shfmt's own diagnostic.
  - Output that is not JSON, or JSON that is not a `File` node, exits with `shfmt gave no JSON AST`.
  - There is no fallback; `--all` refuses too; nothing is baselined.
- **Dialect and targets:**
  - The dialect follows the file: `-ln zsh` for a `.zsh` name or a zsh shebang.
  - A `.tmpl` is a target only when its name without `.tmpl`, or its shebang, is shell or Python.
  - Chezmoi actions are blanked before parsing, with offsets and newlines kept.
- **Deviation from amendment 1's literal text, for the orchestrator to accept or amend:** an `include`, `includeTemplate` or `template` action alone on its line becomes the no-op `:` instead of spaces.
  - **Why:** two tracked templates (`run_after_05-client-install-zed.sh.tmpl`, `run_once_50-client-install-misc.sh.tmpl`) wrap only include lines in a subshell. Blanked to spaces, the subshell is empty and shfmt refuses (`` `(` must be followed by a statement list ``).
  - **Why it is safe:** `:` can neither create nor hide a hit.
  - **Review:** the worker review judged it sound.
- **The walk:**
  - R1 reads `[[ ]]` binary tests and `[`/`test` argument triples.
  - R2 reads `case` words.
  - R5 reads `ps … | grep|awk|cut|sed` pipelines (not `ps -o <f>= -p`) and `pgrep -f` with any parameter expansion, positional and special parameters included.
  - R6 reads `grep -E`/`egrep` without `-F` on an expanding pattern.
  - R3 takes a jq command's program word, skipping option operands (`--arg`/`--argjson`/`--slurpfile`/`--rawfile` 2, `--indent`/`-L`/`--library-path` 1), pure expansions and `-f`. All of the word's literal fragments are concatenated after shell quote removal, each character keeping its source line, and the inherited jq scanner (`jq_mask`, `span`, the normaliser rule) runs on the whole program.
- **Markers:**
  - A marker counts only in an AST comment node on the lines of the hit's statement.
  - A statement's lines are its whole `&&`/`||`/`|` chain's, continued lines included; a `case` runs to its `in`.
  - A normaliser counts in the code, with comments blanked, of those physical lines.
  - Heredoc bodies, the `Hdoc` nodes, are left out of every walk.

## The ten findings (validation §4: red on e520a7fe; §6: green at the head; §5: their mutants)

| Finding | Selector (`tests/unit/test_lint_comparisons.py::LintComparisonsTest::…`) | Red fixtures at e520a7fe | Mutant killed |
| --- | --- | --- | --- |
| audit:b24d313:1 | `test_process_patterns_include_positional_and_special_parameters` | p0 to p5 | M1 |
| audit:b24d313:2 | `test_double_quoted_jq_joins_split_operator_and_path` | so, sp | M2, R1c |
| audit:b24d313:3 | `test_jq_program_concatenates_all_word_parts` | cw, cw2 | M3 |
| audit:b24d313:4 | `test_arithmetic_shift_keeps_following_marker_comments` | as, as2 | M4 |
| audit:b24d313:5 | `test_heredoc_data_is_excluded_from_shell_rules` | hq, hu | M5, M5b |
| audit:b24d313:6 | `test_ansi_c_quotes_preserve_following_marker_comments` | ac | M6 |
| audit:b24d313:7 | `test_all_valid_heredoc_delimiters_exclude_body_markers` | d0, d1, d3 | M7 |
| 4313892754 | `test_a_jq_program_continued_by_backslash_newline_is_located_and_r3_applies` | jc3 (the substitution case) | M8 |
| 4313892766 | `test_a_backslash_newline_joins_the_physical_lines_without_a_separator` | wp (`$` and `1` split) | M9 |
| 4313892783 | `test_a_marker_inside_a_multiline_string_or_heredoc_body_is_not_a_comment` | hd3 (`'END-DATA'`) | M10 |

- **Inherited green controls (pass at e520a7fe, kept):**
  - d2 (`E"N"D`) and d4 (`-'T'`, tab-stripped) in the audit:7 selector;
  - the original Bot reproductions jc, jc2, wj, wc, ms, ms2, hd, hd2;
  - a02's selectors: `test_a_single_quoted_jq_option_value_is_not_read_as_the_program`, `test_a_jq_normaliser_name_inside_a_string_literal_is_no_application`, `test_every_f_string_interpolation_in_a_regex_is_escaped`, and `test_each_owned_row_is_refused_or_accepted_by_its_fixture` with all `OWNED_ROWS` cases including k4;
  - the stale-row selector `test_a_baseline_row_matching_no_hit_fails_as_stale`.
- **Overlap:** the strengthened Bot variants overlap the audit rows. jc3 shares its field split with audit:2, wp shares its parameter reading with audit:1, and hd3 shares its delimiter with audit:7.
- **Refusal and amendment selectors (red at e520a7fe as well):**
  - `test_shfmt_missing_refuses_without_fallback`;
  - `test_shfmt_parse_failure_refuses_with_original_message`, which also covers not-JSON, `{}`, `null` and a non-`File` node;
  - `test_shfmt_falls_back_to_the_pinned_mise_form_with_the_file_dialect_and_blanked_actions`, which also pins PATH-first;
  - `test_the_job_log_records_the_shfmt_probes`, which prints which invocation runs, for validation §11.

## Worker review: correction round 1 of 2 (INV-6, C-61)

The review is recorded in `dotfiles-T129-normalised-comparison-lint-followup-a04-worker-crit.json` and its receipt.

- **The round:** one pre-push review of `b24d3136..c929569b` returned `Verdict: incorrect`, with one P2 and seven P3 items.
- **Fixed in `d74204e6`:**
  - **The P2:** jq hit lines came from decoded text. A `$'…\n…'` program put R3 on a later line, which could raise an IndexError or be accepted by an unrelated marker.
  - the chain scope for markers and normalisers;
  - extglob literals;
  - JSON that is no AST;
  - iterative walks;
  - `${#name}`;
  - double-quote unescaping and PATH-first, each pinned.
- **Fixtures:** the round added four tests: `test_jq_hit_lines_follow_the_source_through_escapes_and_continuations`, `test_a_chained_or_continued_statement_is_one_statement_for_markers_and_normalisers`, `test_an_extglob_pattern_is_literal_text_and_a_length_is_no_path` and `test_a_long_and_chain_is_read_without_recursion`.
- **Mutants:** all 34 are killed (§5).
- **Kept by design:** the heredoc exclusion also drops command substitutions inside unquoted bodies, which bash executes. This follows the Design text "Heredoc bodies are excluded from shell-rule and marker scanning", and is a limit.

## The tracked tree and the baseline (validation §3)

- **`--all`:** at `d74204e6` it is byte-identical to `b24d3136`'s lint: 97 lines, sha256 `8986de4b…`, `diff` exit 0.
  - No baseline row is obsolete and no hit is newly exposed, so a04 leaves `scripts/lint-comparisons-baseline.tsv` unchanged.
- **Parsing:** all 119 shell targets parse.
- **The no-flag lint:** it exits 0 with the eight warnings a02 recorded, all in files this PR leaves unchanged (§8).

## Check (validation §6 to §12)

- **The lint module:** `python3.15 -I -m unittest discover -s tests/unit -p test_lint_comparisons.py -v` passes 33 of 33 (§6).
- **The full suite:** `python3.15 -I -m unittest discover -s tests/unit -v` exits 1 in this sandbox (§7).
  - Every failure is in modules that never run the lint. The causes:
    - temporary-repo `git commit` exits 128;
    - `out of pty devices`;
    - `mktemp` is denied under `/var/folders`;
    - `--base 'main'` does not resolve in a worktree;
    - `-I` keeps the `tests` package from `test_validate_agent_assets`.
  - The lint's two callers pass. CI's `make unit-test` is the suite's authority.
- **`ruff check`:** clean on both files (§9).
- **`make format`:** exits 2 at its first step, shfmt, on 12 files outside this PR (§10). The PR does not change them (`git diff --quiet` exit 0). `ruff format --check` and prettier pass on this PR's files.
- **Caps (§12), over the merge-base `ba318e53`, at `d74204e6` (the records commits add only `.orchestration/` lines):**
  - 304 of 450 changed lines outside `tests/` and `.orchestration/`, without the baseline (`scripts/lint-comparisons.py` +244/−60);
  - 300 of 1200 added under `tests/` (`tests/unit/test_lint_comparisons.py` +300/−4);
  - the baseline, outside the count, +3/−1, all inherited from a02's commits and the chain's main merge; a04 changes no row (`git diff --quiet b24d3136 HEAD -- scripts/lint-comparisons-baseline.tsv`, §12).

## Dependency observations

- **Locally:** PATH's shfmt runs (`~/.local/share/mise/installs/shfmt/latest/shfmt`, v3.14.1); `mise x shfmt@3.14.1 -- shfmt` also answers v3.14.1 (§11).
- **In CI (validation §11, §13), on `09a51c50`, in all four test jobs:** PATH's `shfmt` is a mise shim that exits 1, because no mise config selects a version. The lint runs the pinned `mise x shfmt@3.14.1 -- shfmt` (v3.14.1), and the unit step passes 1286 tests. The fallback in amendment 1 is what makes the unit jobs work without a workflow change.
- **No version pin for PATH's shfmt:** a different version on PATH would be used as amendment 1 orders. Its version is printed, not enforced.

## Blocker: the `regime` check (validation §13)

- **Status:** every test, validate and public-bootstrap job passes, and `regime` fails.
- **Why:** regime-ci collapses a reset_of lineage to its latest copy only when both copies equal their dispatched texts at the base.
  - `origin/main` `ba318e53` holds neither `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a02.md` nor `…-a04.md`, so both copies are unverifiable and a02's copy stays a target.
  - Against that copy, a04's records fall outside its `allowed_files`, and the 304 changed lines exceed the 200-line cap its Check text gives.
  - The fix is outside this task's `allowed_files`: landing the dispatched texts on main (the boundary records), then re-running the job. Neither copy may be edited (the threat table).
- **Also, a warning only:** a04's cap sentence puts the number in `**…**`, which regime-ci's `at most (\d+) changed lines` pattern cannot read ("no outside cap in the copy's ## Check section").

## Limits (residual, as the threat table states)

- Runtime-generated jq programs and parameter-expanded program text are skipped (a `shortcut:` comment marks it).
- Command substitutions inside unquoted heredoc bodies are skipped (Design text).
- A piped `{{ … | include }}`, and a lone include in a case-item position, are outside the `:` rule (none in the tree).
- The lint stays statement-local (`LIMIT`).

## Proposed feedback dispositions (for the orchestrator)

- **audit:b24d313:1 to 7:** `fixed:eb6a58f0` (with `c929569b` and `d74204e6`), each by its selector above.
- **Bot 4313892754, 4313892766, 4313892783:** the original reproductions were already green after f6fd955e. Their strengthened variants (jc3, wp, hd3) are red at e520a7fe and green at `d74204e6`, so the proposal is `fixed:eb6a58f0`.
- **The PR title:** it still names followup-a02. Editing it needs `gh pr edit`, an ask rule this seat does not run.

## Process

- **CompactionDB:** `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "…"` (worktree DB, inside the sandbox; id `141a46eb-96cd-4c11-b3fc-7ab493939ffb`, validation §2). Consolidating it into the main checkout is the orchestrator's acceptance step, since the main checkout's DB is outside this seat's sandbox.
- **Understand-Anything:** no graph-stale hook fired in this task.
- **Plan Mode:** not used.

cost: n/a
