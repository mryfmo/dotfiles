---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a01
seat: claude-standard-dot-a008
branch: lint/normalised-comparisons-followup-a01
base: 68f8a70a
rebased_from: 445c32dd
supersedes: 387
test_commit: c5082855
fix_commit: c33c351f
variable_fix_commit: 85100657
review_test_commit: 18536b1a
review_fix_commit: 514969d1
rereview_test_commit: 10ea506c
rereview_fix_commit: f78e5dbf
baseline_commit: 7fa5d112
pr: pending
task_sha256: 78d582c861315b07f98dc173db1803a20f47e708409cfa4a0f922f82742a7334
---

# Report: dotfiles-T129-normalised-comparison-lint-followup-a01

- Seat: `claude-standard-dot-a008` in `.claude/worktrees/worker-f`; bring-up PING 2026-10-17T17:04:27Z, PONG 17:05:06Z; AGMSG-TASK 17:06:28Z with `task_sha256=ab92d008…`, which the dispatched file and the branch copy `task.md` match byte for byte (validation §1); the task-consistency check passes on it (§1a).
- Branch: the TASK note stacks this branch on PR #387's head `7c8e7484` (the task file's "fresh branch off `origin/main` after PR #387 merges" cannot hold yet: `gh pr view 387` gave `state=OPEN`, `mergedAt=null`, `headRefOid=7c8e7484…` at dispatch); it is rebased onto `origin/main` after #387 merges.
- Amendment 1 (AGMSG-TASK 2026-10-18T09:08:00Z, `task_sha256=78d582c8…`, `previous_task_sha256=ab92d008…`): this task supersedes PR #387 and lands as its own PR against main; the branch copy `task.md` now matches the amended file byte for byte (validation §12). Everything below the Amendment 1 section was written before the rebase and names the pre-rebase commits; validation §12a maps each to its rebased commit (for example 979c0429 is c33c351f, 1b56dc2b is 514969d1, bb60ee84 is f78e5dbf).
- Owned rows: the three rows of `## Owned by dotfiles-T129-normalised-comparison-lint-followup-a01` in `.orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-a01.md`, read at dispatch (4302629300, 4302629305, 4302629307); no row was added after the task text. Each Bot comment was read with `gh api repos/mryfmo/dotfiles/pulls/comments/<id>`.

## Amendment 1 (round 1): the rebase, the baseline, the six #387 threads

1. Rebase (item 1): `git fetch origin main` (one command), then `git rebase origin/main` onto `68f8a70a`: 20 commits replayed with no conflict; the merges 35eff561 and 7c8e7484 drop out, so the PR's diff against main is the whole F2 change (#387's lint and this task's rows). The script and the tests are byte-identical to the pre-rebase tip 445c32dd (§17).
2. Baseline (item 2): on the rebased tree the lint (with the pre-commit baseline) printed four hits and two stale rows (§12b). Commit 7fa5d112 replaces the two stale rows and adds one content-hashed row per hit; the lint then exits 0 with no output (§14) and the tracked-tree test passes (§13). The rows, per rule and per file:
   - `home/dot_claude/hooks/executable_project-map-reload.sh`: R1 at line 40 (`[[ "$event_path" == */.project-map/index.html ]]`), R3 at line 48 (`select(.url | strings | startswith("file://"))`), R1 at line 56 (`[[ "$tab_path" == "$event_path" ]]`). main changed the file after #387's baseline, so its two rows (R1, R3) were stale and are replaced by these three. `dotfiles-T128-project-map-pane-open-a01-followup-a02` lists the file in its allowed_files and has no acceptance record (an owner task written 2026-10-16; I found no dispatch of it), so the owner assignment of these rows is for the orchestrator.
   - `scripts/update-agent-assets.sh`: R2 at line 966 (`case "$(uname -s)/$(uname -m)" in`, from #405), the same content as the existing line-274 row, so the baseline now holds that hash twice (one row per hit). It is an OS/arch string, not a path: a false positive of R2 that the base script reports too. The tasks that list this file all have acceptance records (T129 assets-omp-hcom a01 and its follow-ups, pstack, T132), apart from the legacy T57 to T62b files.
   - No hit is in `scripts/lint-comparisons.py` or the tests.
3. The six Bot threads (item 3), each verified by running its fixture with the lint script of the fix commit's parent (red) and of the fix commit (green) in a scratch worktree at HEAD (§12c), and each thread's own reproducer refused by the lint at HEAD (lint exit 1, §12c):

| Thread (review) | Finding | Fixture | Disposition |
|---|---|---|---|
| 4302545078 (4b843ce9) | one baseline row suppresses many identical hits | `test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails` | `fixed:192c88d2` (#387's df8055ce): red at 480f48c4, green at 192c88d2 |
| 4302545082 (4b843ce9) | a foreign receiver (`fake.realpath`, `fake.escape`) passes as the normaliser | `test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails` | `fixed:192c88d2` (#387's df8055ce): red at 480f48c4 (three cases), green at 192c88d2 |
| 4302545085 (4b843ce9) | the jq normaliser twice on one side passes | `test_the_jq_normaliser_is_required_on_each_operand_side` | `fixed:192c88d2` (#387's df8055ce): red at 480f48c4, green at 192c88d2 |
| 4302629300 (d215e062) | a single-quoted jq option value is read as the program | `test_a_single_quoted_jq_option_value_is_not_read_as_the_program` | `fixed:f78e5dbf` (bb60ee84): the fixture as at c33c351f is red at c5082855 and green at c33c351f; HEAD's widened fixture (the review rounds' forms) is green from f78e5dbf (§12d) |
| 4302629305 (d215e062) | a def name inside a string literal satisfies the side | `test_a_jq_normaliser_name_inside_a_string_literal_is_no_application` | `fixed:514969d1` (1b56dc2b): red at c5082855, green at c33c351f as at that commit; HEAD's fixture (plus the jq comment form) green from 514969d1 |
| 4302629307 (d215e062) | one `re.escape` accepts every interpolation | `test_every_f_string_interpolation_in_a_regex_is_escaped` | `fixed:514969d1` (1b56dc2b): red at c5082855, green at c33c351f as at that commit; HEAD's fixture (plus `map(re.escape, names)`) green from 514969d1 |

4. PR (item 4): see the PR section at the end; the caps hold against `origin/main` (§16): the script 200 of 200, `tests/` 271 added of 1000, the baseline outside the count.

## The owned rows

| Row | Class | Change in `scripts/lint-comparisons.py` at the head `bb60ee84` | Test (red and green: validation §3, §3a, §3b, §3c, §4) |
|---|---|---|---|
| 4302629300 (`:69`) | jq-program-location | `programs()` keeps the base scan (the first single-quoted string after the `jq` word on its logical line) and skips two kinds of candidate: a `'` inside a `"…"` string (`JQ_QUOTE` consumes a closed double-quoted string whole, escape-aware, and backslash escapes and continuations; an unbalanced `"` falls back to plain text as in the base, bb60ee84), and a single-quoted string whose preceding text ends with an option that takes it (`JQ_ARG`: `--arg`, `--argjson`, `--slurpfile`, `--rawfile` with an optional name, `--indent`, `-L`, `--library-path`, from `jq --help` of jq 1.8.2); the next candidate is then read. The `jq` match takes a trailing `"`, `}` or `)` so `"$jq"`, `"${jq}"` and `"$(command -v jq)"` are followed (37bf6a51) | `test_a_single_quoted_jq_option_value_is_not_read_as_the_program`: the Bot's reproducer and `--arg m "${s#*$'\t'}"` refused (red at the base), the normalised form accepted, and twelve forms the base already read kept read (five of them red at 37bf6a51, three at 1b56dc2b) |
| 4302629305 (`:112`) | presence-not-structure | R3 strips string literals (escape-aware) and jq comments from each side, then accepts the side only when the def's name is a whole word there that is no `.field` and no `$variable` (`d in re.findall(r"(?<![\w.$])\w+", side)`) | `test_a_jq_normaliser_name_inside_a_string_literal_is_no_application`: the Bot's reproducer refused (red at the base), a comment naming the def refused (red at 37bf6a51), the applied form accepted |
| 4302629307 (`:144`) | presence-not-structure | Python R6 accepts the call only when every formatted value of the f-string references `re.escape` (`"re.escape" in map(dotted, ast.walk(v))`, so `map(re.escape, names)` counts); an f-string without a formatted value stays a hit, as before | `test_every_f_string_interpolation_in_a_regex_is_escaped`: the Bot's reproducer refused (red at the base), both values escaped accepted, `map(re.escape, names)` accepted (red at 37bf6a51) |

The docstring's last line drops "repo-relative" so its closing quotes share the line and the script stays at 200 lines (D-cap-F2, the TASK note's "trim text if needed"); `--list-rules` is byte-identical to the base (§8).

## re-plan

`re-plan: jq-program-location -> the option-aware word walker (979c0429, 37bf6a51) is replaced by the base scan with two skip rules (1b56dc2b), because three findings of this class reached this artifact: the "$jq" regression found by my own check (fixed in 37bf6a51), and the worker review's two P2 (escaped quotes and nested $( ) in an option's argument, and a fail-open stop at any word the walker did not model, both red at 37bf6a51 in §3b). The walker modelled shell words and read nothing when its model failed; the base scan reads the first single-quoted string whatever precedes it, so skipping candidates on top of it reads every candidate the base reads except a `'` inside a closed `"…"` string (the base's false read at herdr-agents:1195). The worker re-review refuted my first wording of this ("cannot read less than the base"): 1b56dc2b stopped at an unbalanced `"` the base read through (`"$(command -v jq 2>/dev/null)" -r '…'`); bb60ee84 restores the base's reading there. Verification moved with it: every form the reviewer showed the base reading is a guard test, and the edge-shape table (§10a) and the located-set diff (§10) compare the base, 37bf6a51 and the head.`

## The baseline follows

- No hit disappeared, so no row leaves.
- One hit is new (§9): the sharper R6 finds `scripts/orchestrator/task-consistency-check.py:66`, `re.search(rf"(?:{re.escape(rid)}|-{rid.rsplit('-', 1)[-1]})/task\.md", rowtext)`, where the second interpolation is unescaped. The file is owned by no task in flight (last changed by #365); it gets one row (`R6 b2513e6e…`) and its owner is for the lineage's acceptance to assign.

## The located jq programs and the edge shapes (§10, §10a)

- Over every tracked shell file, 86 programs are located by the base and the head alike; the one difference is `home/dot_local/bin/common/executable_herdr-agents:1195`, where the base took the `'\t'` inside `"${seat#*$'\t'}"` for the program and the head reads the real program. `scripts/orchestrator/pr-cost.sh:30` keeps the base's reading of the awk program after `--jq "$2" |` (a false read with no hit, unchanged).
- On fourteen edge shapes (§10a) the base reports lines 1 to 6 and 14, 37bf6a51 reports 7 to 10, 13 and 14, and the head reports every one of them: the head is a superset of both. The re-review's differential fuzz (845,325 shell-balanced lines over 15 jq namings and 39 argument tokens) found the head silent where the base reports R3 only on the unbalanced-quote shapes that bb60ee84 fixes.

## Red before this task, not this task's (closed by Amendment 1's baseline commit)

- `test_the_tracked_tree_is_clean_against_the_baseline` and the Check's lint command fail on `home/dot_claude/hooks/executable_project-map-reload.sh` (three hits, two stale rows) at the head (§4, §5) exactly as with the base script and base baseline on the same tree (§5a): the rows of PR #387's last round, which the TASK note says touches the baseline only.
- The rebase preview (§11) shows one more on `origin/main` `a8a747af`, `scripts/update-agent-assets.sh:960` R2 (`case "$(uname -s)/$(uname -m)" in`, from #388), which the base script reports as well.
- So the Check's "exit 0, no output" and an all-green unit run held only after the rebase; Amendment 1's baseline commit 7fa5d112 closes it (§12b, §13, §14; the line-960 hit is now line 966 on `origin/main` 68f8a70a).

## Caps (§7)

- `scripts/lint-comparisons.py`: 200 lines.
- This task's delta (`7c8e7484...HEAD`): the script 13 added, 12 deleted; the baseline 1 added (outside the count); `tests/` 67 added.
- After the rebase `origin/main...HEAD` holds the whole F2 change, since this PR supersedes #387 (§16): the script 200 (200 of 200), `tests/` 271 added (of 1000), the baseline 88 (outside the count).

## Worker review

An independent read-only reviewer (a fresh general-purpose subagent of this seat, given the task file, the three Bot comments and the commit range, not my conclusions) reviewed `7c8e7484..37bf6a51`: `Verdict: incorrect`, five findings, each dispositioned in `dotfiles-T129-normalised-comparison-lint-followup-a01-worker-crit.json`:

1. P2 row 1, escaped quotes and `a\ b` in an option's argument: fixed in 1b56dc2b (guard tests in be2958cf).
2. P2 row 1, fail-open stop at an unmodelled word (`"${opts[@]}"`, `2>/dev/null`, nested `$( )`, `-r\` continuation): fixed in 1b56dc2b by the re-plan above.
3. P2 row 3, `map(re.escape, names)` and `{3}` refused where the base accepted, `{re.escape(a) + b}` accepted: `map(re.escape, …)` fixed in 1b56dc2b; the other two are residuals below.
4. P3 row 2, a jq comment, `{canonical_path}`, an object key and a def inside a side satisfy the word check: the comment fixed in 1b56dc2b; the rest are residuals below.
5. P3, the docstring edit is outside the owned rows: it is the cap's text trim the TASK note allows; no behaviour, argparse description or `--list-rules` output changes.

Round 2 on `37bf6a51..1b56dc2b`, the same reviewer with its context kept: `Verdict: correct`, four P3. The unbalanced-quote fail-open shape is fixed in bb60ee84 (tests in a0563644, red at 1b56dc2b in §3c); the joined-word option values, the R3 object-key forms and the R6 forms are residuals below. The receipt and the JSON record both rounds.

## Residuals (for the orchestrator's disposition; each stays a residual only because of the 200-line cap)

- R6, within one formatted value: `{re.escape(a) + b}` is accepted (the check is per formatted value, the Bot's stated remedy; a stricter "each value is itself `re.escape(…)`" would refuse `"|".join(re.escape(x) for x in xs)`); a constant value such as `f"{re.escape(a)}{3}"` is refused where the base accepted it.
- R3, the word check still accepts a side where the name is an object key (`{canonical_path: .url}`), the object shorthand `{canonical_path}`, or a `def` inside the side; excluding a word before `:` or after `{` would put the check line over 120 columns and the script over 200 lines.
- Row 1, a single-quoted value joined to other text in one word is still read as the program: `--arg p 'it'\''s'`, `--arg p "$x"'/y'`, `--arg p $'/x'`, `-L'/lib'`, `-nL '/lib'`; the base misses each of these too (no regression), and covering them needs a second option pattern line over the cap.
- R6, a value that only mentions `re.escape` without calling it, such as `{name if re.escape else ''}`, passes the reference check (contrived).
- The tree holds none of these forms (§9 shows the head's hits; the tree's four Python f-string calls are three single `re.escape(x)` values and `'|'.join(forms)`, already a row).

## PR (Amendment 1 item 4)

The `gh pr create` stop of 2026-10-17 no longer matches a live ask rule (D-024-13). After the rebase, the branch is pushed in one command (`--force-with-lease` against 445c32dd), then `gh pr create --draft --repo mryfmo/dotfiles --base main --head lint/normalised-comparisons-followup-a01 --title "…" --body-file .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/pr-body.md` and `gh pr ready <pr>`, each one command. Then CI and the Bot's automatic review are awaited (no `@codex review` comment; 15 minutes without a review is recorded as `bot: none`). PR #387 is closed by the orchestrator when the new PR merges.

CompactionDB: the `memory add` runs at the RESULT, and its command goes into this report then.

cost: n/a
