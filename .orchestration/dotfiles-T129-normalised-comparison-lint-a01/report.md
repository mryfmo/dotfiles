---
task_id: dotfiles-T129-normalised-comparison-lint-a01
seat: claude-review-dot-a005
branch: lint/normalised-comparisons-a01
base: 35ab0e95
code_commit: 4663dc4d
trim_commit: 9fbd0de0
fix_commit: 26ed34bb
rereview_commit: e88f8f05
pr: 387
task_sha256: 0843aafc4d5a64cfa39b2a7fe402d957b3ac6fb10e1c2a1f3fcfa064113d79d0
---

# Report: dotfiles-T129-normalised-comparison-lint-a01

- Seat: `claude-review-dot-a005` in `.claude/worktrees/worker-d`, seated as this task's worker by the operator's instruction (the TASK line's note), on a fresh branch `lint/normalised-comparisons-a01` from `origin/main` `35ab0e95` (boundary (18)).
- Task file: dispatched 2026-10-17T10:24:09Z at `f3bf959c…`; Amendment 1 (TASK line 10:52:00Z, `previous_task_sha256=f3bf959c…`) at `0843aafc…`; Amendment 2 (TASK line 11:04:06Z, `previous_task_sha256=0843aafc…`) at `655e085b…`, copied byte-identical to `task.md`; the task-consistency check passes on it (validation §1a). The three premises replay as recorded (§2a to §2c). One question (PONG 10:44:34Z, answered by Amendment 1), two alive notes on the cap (10:56:53Z and 11:01:41Z, answered by Amendment 2).

## What changed

Validation §5 holds the numstat; the diff is three new files.

- **`scripts/lint-comparisons.py`** (200 lines, standard library only, `python3 -I`): the rule table R0 to R6 of item 1 over the default file set (`git ls-files -z -- home scripts install`, names ending in `.sh`, `.bash`, `.zsh`, `.py` or `.tmpl`, or a `sh`, `bash`, `zsh` or `python` shebang). Shell lines are tokenised with `shlex` after the comment is cut and every `$(...)` folded away; R1 reads a `[[`/`[` test anywhere on the line (so `if [[ … ]]`, `elif`, `&& [[` count), R2 `case … in`, R5 `ps … | grep|awk|cut|sed` (the `ps -o <fields>= -p <pid>` form excepted) and `pgrep -f` on a `$variable`, R6 `grep -E`/`egrep` whose pattern holds `$name` or `${name` (`-F` or `escape_regex` accepted). a jq program is the first single-quoted string after each `jq` word on its logical line (backslash continuations joined, whole-line comments blanked), so a program inside `"$(… | jq '…')"` is read and an apostrophe elsewhere in the file cannot desynchronise the scan; R3 reads `==`, `!=`, `startswith(`, `endswith(`, `ltrimstr(`, `rtrimstr(`, `test(` over the operator's bracket group cut at top-level `,` `;` (and `|` for `==`/`!=`), hit when it holds `.url`, `.path`, a token `$name` or a slash-literal, accepted when a `def canonical_path`/`normalise_*`/`normalize_*` of the program is applied to both sides of that group. Python files go through `ast`: `Compare` with `Eq`/`NotEq`/`In`/`NotIn` and `.startswith`/`.endswith` calls (R4), `re.compile|search|match|fullmatch` on an f-string without `re.escape` (R6). The operand rule is Amendment 1's: a literal with `/`, `~`, `file://`, `.html` or `%2F`, or an identifier with a whole segment (split at `_`, `.`, `-` and lower-to-upper changes) equal to a token or its plural. The marker `# lint-comparisons: allow <reason>` accepts the line (for jq, the hit line or the program's first line); a bare marker is R0. `--list-rules` prints the seven rows and the statement-local limit. Output is sorted by path and line; with explicit file arguments only the scanned files' rows can be stale.
- **`scripts/lint-comparisons-baseline.tsv`** (85 rows): one content-hashed row per distinct hit on `origin/main` after Amendment 1 (86 hits; two identical lines of remove-agent-asset share one row), the four premise-3 lines among them; a row matching no hit fails as `stale baseline row <path> <rule id>`.
- **`tests/unit/test_lint_comparisons.py`** (160 lines, 3 tests, stdlib only, the lint as a `python3 -I` subprocess on fixtures in a temporary directory and on the checkout): item 3's three tests, named below.

## The question, the amendment and the cap

1. The lint as first specified (the substring token rule) printed 87 hits on the tree, the four baseline lines among them; the other 83 sat in files no in-flight task owns, so item 2's definition admitted none and test 3 could not pass. Question 1 (PONG 10:44:34Z; the list with source lines in `question-1.md`) named the two systematic sources (the substring rule on `profile`, `profiles`, `HOMEBREW_INSTALL_SHA256`; slash literals that are URLs or version strings) and three options.
2. Amendment 1 (10:52:00Z): the token rule becomes a segment match; the baseline carries every remaining hit; the RESULT lists the rows per rule and per file for the orchestrator to assign owners; nothing is fixed in this PR; the rule table, the tests and the caps are unchanged.
3. The segment rule left 73 hits at the first push; the worker review (below) found two scan defects whose fix adds 13 (`if [[ … ]]` and `elif`/`&& [[` forms, and `case "$(uname -s)/$(uname -m)"`): the baseline carries the 86 hits (R1 33, R2 2, R3 6, R4 41, R6 4; 29 files) as 85 rows (R1 32: remove-agent-asset's two identical lines are one row); `baseline-rows.md` lists each hit with its source line. Between the first two runs a scan defect of mine had dropped every R3 (the quoted-region scan indexed a comment-blanked copy while the line count read the original); the four premise-3 lines were the check that exposed it, and the fixed scan recovers the six R3 rows.
4. The cap: `git diff --numstat origin/main...HEAD` gives 211 + 73 = 284 changed lines outside `tests/` and `.orchestration/` against the Check's 200 (the script alone is 211); reported by PONG at 10:56:53Z (with a wrong parenthetical, corrected at 11:01:41Z). Amendment 2 (TASK line 11:04:06Z, task `655e085b…`; decision D-cap-F2): the baseline TSV is data and leaves the 200 count, and the script alone must be at most 200 lines with no rule, test or behaviour removed. The trim (`9fbd0de0`: the segment token rule as one regex, the shell quote scan as one regex, the R0 dedupe left to the caller's set) brings the script to 198 lines; the tree yields the same 73 hits (checked by diffing the hit lists before and after) and the three tests stay green (validation §3, §5a).

## The rows per rule and per file (the baseline; item 2; rows, not hits: remove-agent-asset's two identical lines are one row)

| rule | rows |
|---|--:|
| R1 | 32 |
| R2 | 2 |
| R3 | 6 |
| R4 | 41 |
| R6 | 4 |

| file | rows (rules) |
|---|---|
| scripts/validate-agent-assets.py | 16 (R4 ×15, R6) |
| home/dot_local/bin/common/executable_herdr-agents | 12 (R1 ×8, R3 ×3, R6) |
| home/dot_local/bin/common/executable_ua-symbol-coverage | 10 (R4 ×10) |
| scripts/orchestrator/dispatch.sh | 5 (R1 ×5) |
| scripts/require-crit-review.py | 5 (R4 ×5) |
| scripts/check-agent-runtime.py | 4 (R4 ×4) |
| install/ubuntu/common/aws_cli.sh | 3 (R1 ×3) |
| scripts/generate-docs.sh | 3 (R1 ×2, R2) |
| home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py | 2 (R4 ×2) |
| home/dot_claude/hooks/executable_project-map-reload.sh | 2 (R1, R3; PR #379's lineage) |
| home/dot_local/bin/common/executable_remove-agent-asset | 2 (R1 ×2; its two R1 hits share one row) |
| scripts/agent-stop-gate.sh | 2 (R1 ×2) |
| scripts/orchestrator/local-review.sh | 2 (R1 ×2) |
| scripts/orchestrator/task-consistency-check.py | 2 (R4 ×2) |
| home/dot_local/bin/common/executable_agent-session-staleness | 1 (R4) |
| install/ubuntu/client/default_shell.sh | 1 (R1) |
| scripts/check-regime-boundary.sh | 1 (R3) |
| scripts/generate-agent-configs.py | 1 (R4) |
| scripts/gh-auth.sh | 1 (R1) |
| scripts/lib/asset-manifest.sh | 1 (R1) |
| scripts/lib/github-release.sh | 1 (R1) |
| scripts/orchestrator/chain-integrate.sh | 1 (R1) |
| scripts/orchestrator/ledger-check.py | 1 (R4) |
| scripts/orchestrator/local-advisory.sh | 1 (R6; the chain-review a04 owner) |
| scripts/orchestrator/orch-gate.sh | 1 (R1) |
| scripts/orchestrator/pr-cost.sh | 1 (R6) |
| scripts/orchestrator/resolve-threads.sh | 1 (R3; PR #375's lineage) |
| scripts/update-agent-assets.sh | 1 (R2) |
| scripts/upgrade-tools.sh | 1 (R1) |

## Tests

| Test | What it pins |
|---|---|
| `test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted` | each row's fixture refused with its id as the only hit (R0 to R6, plus the Python form of R6); one accepted form per normaliser of each row's Allowed column (ten for R1 and R2, three for R3, eleven for R4 including `os.path.samefile`, two for R5, two for R6 and `re.escape`); the marker with a reason accepted and the bare marker refused as R0; `--list-rules` printing R0 to R6 and the shortcut line |
| `test_a_baseline_row_matching_no_hit_fails_as_stale` | a baseline row naming a fixture's line passes it; the same baseline against the fixture with that line changed fails with `stale baseline row <path> R1` and the new hit |
| `test_the_tracked_tree_is_clean_against_the_baseline` | the lint over the default file set of the checkout with the committed baseline: exit 0, no output (the CI gate under `make unit-test`) |

## Readings, declared

- A Python operand is read by its own name: `ast.Name` by `id`, `ast.Attribute` by `attr` (so `proc.returncode` is not a path operand; `path.suffix == ".md"` is not a hit); a `$(...)` in shell is never an operand (a normaliser inside it accepts the statement through the statement-wide check).
- "The same statement wraps the operand" is read as: the normaliser appears in the statement's text (shell: the line; jq: the operator's bracket group; Python: the operand's subtree). The `--list-rules` shortcut line names the cross-line limit.
- A jq program is a single-quoted region whose logical line holds the word `jq`; `"\(…)"` interpolations are dropped before the slash-literal check, so a division inside a string is no slash.
- The file set's shebang rule is the task's: `#!/usr/bin/env -S uv run --script` is none of `sh`, `bash`, `zsh`, `python`, so that one executable is outside the set. A `.tmpl` is read by its inner extension or shebang; a Python file that does not parse (a template) yields only R0.
- Rows are keyed by path, rule and the hash of the stripped line; the same text twice in one file is one row that both hits match.

## Review, hook, cost

- Worker-side independent review (a fresh read-only subagent given the diff and the task file; three rounds with its context kept; the records in `dotfiles-T129-normalised-comparison-lint-a01-worker-crit.json`, the receipt beside it): round 1 on 4663dc4d and 9fbd0de0 `incorrect` (two P1: the test word only at line start, the whole-file quote pairing of the jq scan; five P2; ten P3), fixed in `26ed34bb`; round 2 on 26ed34bb `incorrect` (one P2 and one P3 of mine claimed fixed but not in the diff: two unasserted string replacements had missed the formatted text; three new P3), fixed in `e88f8f05`; round 3 on e88f8f05 `correct`, one new P3 declared (the three `python3 -I -c` R2 accepted forms pass vacuously because a substitution holding parentheses is not folded, so a `case` word with such a substitution is unchecked). The cap is why the declared P3s stay: the script is at 200 lines.
- No Understand-Anything hook prompt fired in this session; no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
- CompactionDB: one decision added in this worktree's store before completion, id `53f1d551-ba19-4a5d-817c-984f1a801a4a` (validation §6); the orchestrator consolidates adopted decisions into the main checkout's store at acceptance.
