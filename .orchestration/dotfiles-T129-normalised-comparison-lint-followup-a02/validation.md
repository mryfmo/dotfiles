---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a02
seat: claude-standard-dot-a008
code_head: 5b6c5a8a
revise_1_code_head: f6fd955e
revise_1_previous_head: 1950a4de087261dbfe5bac526de9b9285f7717af
base: 51ba5801
---

# Validation: dotfiles-T129-normalised-comparison-lint-followup-a02

- Every block ran inside the sandbox from this worktree on `tools/lint-comparisons-followup-a02` at the code head `5b6c5a8a`. Each block prints its commands, their verbatim output and the block's last exit status. The only later commit adds this directory's records.
- `MAIN` names the main checkout, `T` the task id, and `BASE` the merge-base `51ba5801`. The scratch worktrees under `$TMPDIR` are removed after their block with `git worktree remove --force` (`git worktree prune` never ran).
- **Red, in two steps:**
  - §4 is the owned-row fixtures at `75c3c55c`, whose lint is main's.
  - §4b is the worker review's forms at `3b59177f`, whose lint is the first implementation `607d4485`'s.
  - §5 and §5a are green at the code head.
- **§12 to §12b** are process row audit:4f5be51:12: `make format` verbatim, at HEAD and at the merge-base, with per-file exit statuses. Its exit 2 is inherited, the same twelve files at both.

## 1. Task file (amendment 1, sha256 4198ddc1…) and the branch copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
4198ddc1b8b5e30a66c89ba01e4051a65758806f6d15d0e5dd495876902fca98  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a02.md
4198ddc1b8b5e30a66c89ba01e4051a65758806f6d15d0e5dd495876902fca98  .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a02/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-normalised-comparison-lint-followup-a02.md: OK
[exit 0]
```
## 2. Branch, origin/main, merge-base and this task's commits
```console
$ git branch --show-current; git rev-parse HEAD origin/main; git merge-base origin/main HEAD; git log --oneline origin/main..HEAD
tools/lint-comparisons-followup-a02
5b6c5a8acc707ca0d39f6ea0771e240c71570e09
51ba580149fcace54a912358e7e87c5b07cd8760
51ba580149fcace54a912358e7e87c5b07cd8760
5b6c5a8a fix(lint): the worker review's round: the jq scanner steps escapes by two and characters by one, if-end is one operand, shell words decide pgrep and grep expansion, markers past a continuation or a closing quote and in jq comments, multi-line double-quoted programs, no program past a separator, a constant join separator, odd trailing backslashes (T129 normalised-comparison-lint followup a02, worker review)
3b59177f test(lint): the worker review's forms per gap: markers past a continuation or a quote's line, escaped backslashes, multi-line and post-separator jq programs, a raw join separator, if-end operands, quoted grep pieces, long jq literals, mixed-quote pgrep (T129 normalised-comparison-lint followup a02, worker review)
607d4485 fix(lint): the comparison lint reads tokens: continuation lines join, markers count only in comments, a jq scanner skips strings and comments and bounds operands by and/or and if/then/else, double-quoted jq programs, every escaped fragment, quoted pgrep patterns, single-quoted grep patterns, literal path pieces beside expansions (T129 normalised-comparison-lint followup a02)
75c3c55c test(lint): one entry per distinct gap naming its row ids, a Bot row and its local twin closed by the same fixture (T129 normalised-comparison-lint followup a02, amendment 1)
bb748444 chore(orchestration): the amendment 1 task copy, byte-identical (T129 normalised-comparison-lint followup a02)
883a6ab8 test(lint): one fixture per owned row of the F2 lineage (four Bot rows of #415, nine audit rows of 4f5be51), each red against main's lint; the byte-identical task copy (T129 normalised-comparison-lint followup a02)
[exit 0]
```
## 3. The owned rows as the two records hold them
```console
$ for r in followup-a01 followup-a03; do awk "/^## Owned by $T/{f=1} f&&/^## /&&!/Owned by $T/{exit} f" "$MAIN/.orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-$r.md" | cut -c1-180; done
## Owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (advisory P2 of PR #415; rows id<TAB>class)

4306643800	multiline-shell-test
4306643803	double-quoted-jq-program
4306643804	mixed-escaped-raw-name
4306643808	marker-in-string

## Owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:4f5be51:1	advisory-p2
local-finding: 4f5be51:1 not-applicable:advisory P2 owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (- [P2] Bound jq operands at logical comparison boundaries — scri
local:4f5be51:2	advisory-p2
local-finding: 4f5be51:2 not-applicable:advisory P2 owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (- [P2] Check every dynamic fragment within a regex interpolation
local:4f5be51:3	advisory-p2
local-finding: 4f5be51:3 not-applicable:advisory P2 owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (- [P2] Exclude literal dollar signs from shell interpolation che
local:4f5be51:4	advisory-p2
local-finding: 4f5be51:4 not-applicable:advisory P2 owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (- [P2] Fold shell continuations before checking comparison token
local:4f5be51:5	advisory-p2
local-finding: 4f5be51:5 not-applicable:advisory P2 owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (- [P2] Ignore jq literals and comments when locating operators —
local:4f5be51:6	advisory-p2
local-finding: 4f5be51:6 not-applicable:advisory P2 owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (- [P2] Inspect the complete quoted pattern passed to pgrep — scr
local:4f5be51:7	advisory-p2
local-finding: 4f5be51:7 not-applicable:advisory P2 owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (- [P2] Preserve literal path suffixes after variable expansions 
local:4f5be51:8	advisory-p2
local-finding: 4f5be51:8 not-applicable:advisory P2 owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (- [P2] Recognize allow markers only in actual comments — scripts
local:4f5be51:9	advisory-p2
local-finding: 4f5be51:9 not-applicable:advisory P2 owned by dotfiles-T129-normalised-comparison-lint-followup-a02 (- [P2] Recognize double-quoted jq programs — scripts/lint-compar
- 2026-10-19T05:30Z: the chain re-run stopped again at the sweep: the regime check-run item and its annotation share one URL, which fill_sweep refuses as a key ("shared-key") and n

[exit 0]
```
## 4. RED: the owned-row fixtures at the tests commit 75c3c55c, whose lint is origin/main's, in a scratch worktree
```console
$ git -C "$R" diff --quiet $BASE -- scripts && echo "scripts identical to $BASE"; cd "$R" && uv run python -m unittest $OWN 2>&1 | /usr/bin/grep -E "^FAIL:|^Ran|^(OK|FAILED)" | sed -E "s/ \(tests\.unit\.test_lint_comparisons\.LintComparisonsTest\.[a-z_]+\)//"
scripts identical to 51ba5801
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643800 audit:4f5be51:4', fixture='c.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643803 audit:4f5be51:9', fixture='j.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643804 audit:4f5be51:2', fixture='r.py')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643808 audit:4f5be51:8', fixture='m.py')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643808 audit:4f5be51:8', fixture='k.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='audit:4f5be51:1', fixture='l.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='audit:4f5be51:3', fixture='g.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='audit:4f5be51:5', fixture='s.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='audit:4f5be51:6', fixture='p.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='audit:4f5be51:7', fixture='v.sh')
Ran 1 test in 0.435s
FAILED (failures=10)
[exit 0]
```
## 4b. RED: the worker review's forms at their tests commit 3b59177f, whose lint is the first implementation 607d4485's, in a scratch worktree
```console
$ git -C "$R2" diff --quiet 607d4485 -- scripts && echo "scripts identical to 607d4485"; cd "$R2" && uv run python -m unittest $OWN 2>&1 | /usr/bin/grep -E "^FAIL:|^Ran|^(OK|FAILED)" | sed -E "s/ \\(tests\\.unit\\.test_lint_comparisons\\.LintComparisonsTest\\.[a-z_]+\\)//"
scripts identical to 607d4485
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643800 audit:4f5be51:4', fixture='c2.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643800 audit:4f5be51:4', fixture='c3.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643803 audit:4f5be51:9', fixture='j2.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643803 audit:4f5be51:9', fixture='j3.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643804 audit:4f5be51:2', fixture='r2.py')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='4306643808 audit:4f5be51:8', fixture='k2.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='audit:4f5be51:1', fixture='l2.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='audit:4f5be51:3', fixture='g2.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='audit:4f5be51:5', fixture='s2.sh')
FAIL: test_each_owned_row_is_refused_or_accepted_by_its_fixture (rows='audit:4f5be51:6', fixture='p2.sh')
Ran 1 test in 0.894s
FAILED (failures=10)
[exit 0]
```
## 5. GREEN: the Check's unit command at HEAD, verbose
```console
$ git rev-parse --short=8 HEAD; uv run python -m unittest tests/unit/test_lint_comparisons.py -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
5b6c5a8a
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_hit_in_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_in_a_changed_file_fails) ... ok
test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... ok
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... ok
test_a_stale_row_for_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_a_changed_file_fails) ... ok
test_a_stale_row_for_an_unchanged_file_warns (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_an_unchanged_file_warns) ... ok
test_each_owned_row_is_refused_or_accepted_by_its_fixture (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_owned_row_is_refused_or_accepted_by_its_fixture) ... ok
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (tests.unit.test_lint_comparisons.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... ok
test_the_changed_files_are_clean_against_the_baseline (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_changed_files_are_clean_against_the_baseline) ... ok
test_the_jq_normaliser_is_required_on_each_operand_side (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails) ... ok
Ran 15 tests in 6.449s
OK
[exit 0]
```
## 5a. Each fix is load-bearing: one mutant per gap reverts it, and its own fixture entry fails (the mutant script, then its run)
```console
$ cat "$TMPDIR/mut-l02.py"; uv run --no-project python -I "$TMPDIR/mut-l02.py" "$Q"
# Each mutant reverts one fix of followup-a02 (the gaps, then the worker review's round); its fixture must fail.
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); f = root / "scripts/lint-comparisons.py"; src = f.read_text()
M = {  # what the mutant reverts -> (the fixed text, the mutant)
    "continuations (4306643800 audit:4f5be51:4)": ('if (len(code) - len(code.rstrip("\\\\"))) % 2:', 'if False:'),
    "shell markers in comments (audit:4f5be51:8 k.sh)": ('return {n: comment(raw) for n, raw in', 'return {n: raw for n, raw in'),
    "python markers in comment tokens (4306643808 m.py)": ('return {t.start[0]: t.string for t in toks if t.type == tokenize.COMMENT}',
                                                        'return dict(enumerate(text.split("\\n"), 1))'),
    "jq strings and comments (audit:4f5be51:5)": ('bare, lits = jq_mask(prog)', 'bare, lits = prog, prog'),
    "and/or bounds (audit:4f5be51:1)": ('(?:and|or|then|elif|else)(?!\\w)"', '(?!)"'),
    "double-quoted programs (4306643803 audit:4f5be51:9)": ("""('[^']*'|"(?:[^"\\\\]|\\\\[\\s\\S])*")""", "('[^']*')"),
    "every escaped fragment (4306643804 audit:4f5be51:2)": ('all(map(escaped, values))', 'all("re.escape" in map(dotted, ast.walk(v)) for v in values)'),
    "the pgrep pattern word expands (audit:4f5be51:6)": ('any(map(expands, PGREP.findall(line)))', 'any("$" in w for w in PGREP.findall(line))'),
    "the grep pattern word expands (audit:4f5be51:3)": ('if ere and expands(pattern)', 'if ere and "$" in pattern'),
    "path pieces beside expansions (audit:4f5be51:7)": ('return bool(name and TOKEN.search(name.group(1))) or bool(',
                                                      'return bool(TOKEN.search(name.group(1))) if name else bool('),
    "review: one slot per string character, the P1 (s2.sh)": ('code[i : i + step], lits[i : i + step] = [" "] * step, prog[i : i + step]',
                                                          'code[i], lits[i : i + len(two)] = " ", (two if c == "\\\\" else c)'),
    "review: if...end is one operand (l2.sh)": ('"( ", re.sub(r"(?<![\\w.$])end(?!\\w)", "  )", bare)', '"; ", re.sub(r"(?<![\\w.$])end(?!\\w)", "  ;", bare)'),
    "review: a marker on any line of a continued statement (c2.sh)": ('for k in range(n, last + 1)', 'for k in range(n, n + 1)'),
    "review: a shell comment past the closing quote (k2.sh)": ('after = comment(code[close:].split("\\n", 1)[0])', 'after = ""'),
    "review: no program past a separator (j3.sh)": ("""[^'"\\\\\\n;&|])*+""", """[^'"\\\\\\n])*+"""),
    "review: a quote ending its line opens a program (j2.sh)": ('(?=[^\\n]*\\S)', ''),
    "review: a join's separator is a constant (r2.py)": (' and isinstance(node.func.value, ast.Constant)', ''),
}
test = "tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_owned_row_is_refused_or_accepted_by_its_fixture"
for name, (a, b) in M.items():
    assert src.count(a) == 1, (name, src.count(a))
    f.write_text(src.replace(a, b))
    r = subprocess.run(["uv", "run", "python", "-m", "unittest", test], cwd=root, capture_output=True, text=True)
    failed = sorted({l.split("fixture=")[1].rstrip(")") for l in r.stderr.splitlines() if l.startswith("FAIL") and "fixture=" in l})
    print(f"{name}: {'killed' if r.returncode else 'SURVIVED'}; failing fixtures: {', '.join(failed) or '-'}")
f.write_text(src)
continuations (4306643800 audit:4f5be51:4): killed; failing fixtures: 'c.sh'
shell markers in comments (audit:4f5be51:8 k.sh): killed; failing fixtures: 'k.sh', 'k3.sh'
python markers in comment tokens (4306643808 m.py): killed; failing fixtures: 'm.py'
jq strings and comments (audit:4f5be51:5): killed; failing fixtures: 's.sh'
and/or bounds (audit:4f5be51:1): killed; failing fixtures: 'l.sh'
double-quoted programs (4306643803 audit:4f5be51:9): killed; failing fixtures: 'j.sh', 'j2.sh'
every escaped fragment (4306643804 audit:4f5be51:2): killed; failing fixtures: 'r.py', 'r2.py'
the pgrep pattern word expands (audit:4f5be51:6): killed; failing fixtures: 'p2.sh'
the grep pattern word expands (audit:4f5be51:3): killed; failing fixtures: 'g.sh'
path pieces beside expansions (audit:4f5be51:7): killed; failing fixtures: 'v.sh'
review: one slot per string character, the P1 (s2.sh): killed; failing fixtures: 's2.sh'
review: if...end is one operand (l2.sh): killed; failing fixtures: 'l2.sh'
review: a marker on any line of a continued statement (c2.sh): killed; failing fixtures: 'c2.sh'
review: a shell comment past the closing quote (k2.sh): killed; failing fixtures: 'k2.sh'
review: no program past a separator (j3.sh): killed; failing fixtures: 'j3.sh'
review: a quote ending its line opens a program (j2.sh): killed; failing fixtures: 'j2.sh'
review: a join's separator is a constant (r2.py): killed; failing fixtures: 'r2.py'
[exit 0]
```
## 6. The Check's lint at HEAD, no mode flag: exit 0; its output is warnings for unchanged files only
```console
$ uv run --no-project python -I scripts/lint-comparisons.py; echo "lint exit $?"
warning: scripts/check-regime-boundary.sh:125: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
warning: scripts/orchestrator/chain-integrate.sh:93: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
warning: scripts/orchestrator/chain-integrate.sh:106: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
warning: scripts/orchestrator/regime-ci.py:65: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
warning: scripts/orchestrator/regime-ci.py:71: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:72: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:90: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:246: R4 Python compares a path or URL by its string form
warning: 8 unbaselined hit(s) and 0 stale row(s) in unchanged files
lint exit 0
[exit 0]
```
## 7. The lint --all at HEAD
```console
$ uv run --no-project python -I scripts/lint-comparisons.py --all; echo "lint --all exit $?"
home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py:559: R4 Python compares a path or URL by its string form (baseline)
home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py:575: R4 Python compares a path or URL by its string form (baseline)
home/dot_claude/hooks/executable_project-map-reload.sh:40: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_claude/hooks/executable_project-map-reload.sh:48: R3 jq compares a URL or path by its string form (baseline)
home/dot_claude/hooks/executable_project-map-reload.sh:56: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_agent-session-staleness:71: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:416: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:539: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:760: R3 jq compares a URL or path by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:992: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1186: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1233: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1309: R3 jq compares a URL or path by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1395: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1717: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1843: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:1846: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:2050: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
home/dot_local/bin/common/executable_herdr-agents:2117: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:90: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:92: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:94: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:170: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:172: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:218: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:230: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:236: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:239: R4 Python compares a path or URL by its string form (baseline)
home/dot_local/bin/common/executable_ua-symbol-coverage:241: R4 Python compares a path or URL by its string form (baseline)
install/common/mise.sh:45: R2 shell case matches a path or URL operand by its string form (baseline)
install/macos/common/brew.sh:82: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
install/macos/common/brew.sh:91: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
install/ubuntu/client/default_shell.sh:17: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
install/ubuntu/common/aws_cli.sh:66: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
install/ubuntu/common/aws_cli.sh:81: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
install/ubuntu/common/aws_cli.sh:161: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/agent-stop-gate.sh:114: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/agent-stop-gate.sh:126: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/check-agent-runtime.py:133: R4 Python compares a path or URL by its string form (baseline)
scripts/check-agent-runtime.py:134: R4 Python compares a path or URL by its string form (baseline)
scripts/check-agent-runtime.py:677: R4 Python compares a path or URL by its string form (baseline)
scripts/check-agent-runtime.py:679: R4 Python compares a path or URL by its string form (baseline)
scripts/check-regime-boundary.sh:125: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
scripts/check-regime-boundary.sh:191: R3 jq compares a URL or path by its string form (baseline)
scripts/generate-agent-configs.py:1378: R4 Python compares a path or URL by its string form (baseline)
scripts/generate-docs.sh:129: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/generate-docs.sh:145: R2 shell case matches a path or URL operand by its string form (baseline)
scripts/generate-docs.sh:518: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/gh-auth.sh:50: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/lib/asset-manifest.sh:75: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/lib/github-release.sh:28: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/chain-integrate.sh:69: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/chain-integrate.sh:93: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
scripts/orchestrator/chain-integrate.sh:106: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
scripts/orchestrator/ci-rerun.sh:117: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
scripts/orchestrator/dispatch.sh:109: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/dispatch.sh:190: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/dispatch.sh:202: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/dispatch.sh:209: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/dispatch.sh:334: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/ledger-check.py:25: R4 Python compares a path or URL by its string form (baseline)
scripts/orchestrator/local-review.sh:82: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/local-review.sh:83: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/orch-gate.sh:72: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/orchestrator/pr-cost.sh:49: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
scripts/orchestrator/regime-ci.py:65: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
scripts/orchestrator/regime-ci.py:71: R4 Python compares a path or URL by its string form
scripts/orchestrator/regime-ci.py:72: R4 Python compares a path or URL by its string form
scripts/orchestrator/regime-ci.py:90: R4 Python compares a path or URL by its string form
scripts/orchestrator/regime-ci.py:246: R4 Python compares a path or URL by its string form
scripts/orchestrator/resolve-threads.sh:45: R3 jq compares a URL or path by its string form (baseline)
scripts/orchestrator/task-consistency-check.py:56: R4 Python compares a path or URL by its string form (baseline)
scripts/orchestrator/task-consistency-check.py:66: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
scripts/orchestrator/task-consistency-check.py:118: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:159: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:251: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:258: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:260: R4 Python compares a path or URL by its string form (baseline)
scripts/require-crit-review.py:1066: R4 Python compares a path or URL by its string form (baseline)
scripts/upgrade-tools.sh:283: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form (baseline)
scripts/validate-agent-assets.py:115: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:268: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:317: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:321: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:377: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:403: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:475: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:504: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:506: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:509: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:511: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:823: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:1059: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:1330: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:1405: R4 Python compares a path or URL by its string form (baseline)
scripts/validate-agent-assets.py:1408: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string) (baseline)
lint --all exit 0
[exit 0]
```
## 8. What the sharper rules change on the tracked tree: --all of origin/main's lint (a scratch worktree at 51ba5801) against HEAD's, as file and rule counts, then the baseline diff
```console
$ (cd "$B2" && uv run --no-project python -I scripts/lint-comparisons.py --all) > "$TMPDIR/l02-a.txt"; uv run --no-project python -I scripts/lint-comparisons.py --all > "$TMPDIR/l02-b.txt"; for f in a b; do sed -E "s/^([^:]+):[0-9]+: (R[0-9]).*\((baseline)\)$/\1 \2 baseline/; s/^([^:]+):[0-9]+: (R[0-9]).*/\1 \2 unbaselined/" "$TMPDIR/l02-$f.txt" | sort | uniq -c > "$TMPDIR/l02-$f.cnt"; done; diff "$TMPDIR/l02-a.cnt" "$TMPDIR/l02-b.cnt"; echo "(< main, > head)"; git diff $BASE HEAD -- scripts/lint-comparisons-baseline.tsv | /usr/bin/grep "^[-+][^-+]"
6c6
<    3 home/dot_local/bin/common/executable_herdr-agents R3 baseline
---
>    2 home/dot_local/bin/common/executable_herdr-agents R3 baseline
8a9,10
>    1 install/common/mise.sh R2 baseline
>    2 install/macos/common/brew.sh R1 baseline
12a15
>    1 scripts/check-regime-boundary.sh R1 unbaselined
20a24
>    2 scripts/orchestrator/chain-integrate.sh R1 unbaselined
(< main, > head)
-home/dot_local/bin/common/executable_herdr-agents	R3	de8d2d7c93d68b7d8ddeef07ba996751b9ea5d73923798f0e38f12e2bc6f335f
+install/common/mise.sh	R2	ed128028f413f99becb2e87f16b65d0bdf403344a88859025304b3ef44ce9633
+install/macos/common/brew.sh	R1	d64dcec054d4c6610d4b4889df26e5a4c6dae1acb15185b044500416f6e22cc4
+install/macos/common/brew.sh	R1	d64dcec054d4c6610d4b4889df26e5a4c6dae1acb15185b044500416f6e22cc4
[exit 0]
```
## 9. --list-rules is byte-identical to origin/main's (the rule table and the LIMIT line)
```console
$ git show $BASE:scripts/lint-comparisons.py > "$TMPDIR/lm.py"; uv run --no-project python -I "$TMPDIR/lm.py" --list-rules > "$TMPDIR/r-old.txt"; uv run --no-project python -I scripts/lint-comparisons.py --list-rules > "$TMPDIR/r-new.txt"; cmp "$TMPDIR/r-old.txt" "$TMPDIR/r-new.txt" && echo "--list-rules identical"
--list-rules identical
[exit 0]
```
## 10. The Check's ruff check, and ruff format --check, on the two files
```console
$ ruff check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py; echo "ruff check exit $?"; ruff format --config ruff.toml --check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py; echo "ruff format exit $?"
All checks passed!
ruff check exit 0
2 files already formatted
ruff format exit 0
[exit 0]
```
## 11. Caps over origin/main...HEAD (additions plus deletions; the baseline outside the first count) and the changed files
```console
$ B=$(git merge-base origin/main HEAD); echo "merge-base ${B:0:8}"; git diff --numstat "$B...HEAD"; git diff --numstat "$B...HEAD" | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1 + \$2; next} \$3 == \"scripts/lint-comparisons-baseline.tsv\" {b += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/, without the baseline: %d of 350\nunder tests/: %d of 1000\nthe baseline (outside the count): %d\n\", o, t, b}"; echo "script lines: $(wc -l < scripts/lint-comparisons.py)"
merge-base 51ba5801
82	0	.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a02/task.md
3	1	scripts/lint-comparisons-baseline.tsv
131	32	scripts/lint-comparisons.py
68	0	tests/unit/test_lint_comparisons.py
outside tests/ and .orchestration/, without the baseline: 163 of 350
under tests/: 68 of 1000
the baseline (outside the count): 4
script lines:      326
[exit 0]
```
## 12. make format at HEAD 5b6c5a8a, verbatim
```console
$ make format
shfmt --indent 4 --space-redirects --diff .
diff .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh.orig .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
@@ -7,13 +7,16 @@
 F=.orchestration/metrics/pr-cost.tsv
 [ -s "$F" ] || printf 'pr\tbranch\tcreated\tmerged\twall_h\tcommits\tbot_reviews\tp1\tp2\tlocal_reviews\tboundary_updates\trecorded_at\n' > "$F"
 j=$(gh api "repos/mryfmo/dotfiles/pulls/$pr")
-branch=$(jq -r .head.ref <<<"$j"); created=$(jq -r .created_at <<<"$j"); merged=$(jq -r '.merged_at // ""' <<<"$j"); commits=$(jq -r .commits <<<"$j")
+branch=$(jq -r .head.ref <<< "$j")
+created=$(jq -r .created_at <<< "$j")
+merged=$(jq -r '.merged_at // ""' <<< "$j")
+commits=$(jq -r .commits <<< "$j")
 end=${merged:-$(date -u +%FT%TZ)}
 wall=$(uv run --no-project python -c "import sys,datetime as d;a,b=[d.datetime.fromisoformat(x.replace('Z','+00:00')) for x in sys.argv[1:3]];print(round((b-a).total_seconds()/3600,1))" "$created" "$end")
 bot=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/reviews" --paginate --jq '[.[] | select(.user.login=="chatgpt-codex-connector[bot]")] | length')
 p1=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/comments" --paginate --jq '[.[] | select(.in_reply_to_id==null and .user.login=="chatgpt-codex-connector[bot]") | select(.body | test("P[01] Badge"))] | length')
 p2=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/comments" --paginate --jq '[.[] | select(.in_reply_to_id==null and .user.login=="chatgpt-codex-connector[bot]") | select(.body | test("P[23] Badge"))] | length')
-local_n=$({ /usr/bin/grep -l -E "^pr: $pr\$" .orchestration/validation/*local-review-*.md 2>/dev/null || true; } | wc -l | tr -d " ")
+local_n=$({ /usr/bin/grep -l -E "^pr: $pr\$" .orchestration/validation/*local-review-*.md 2> /dev/null || true; } | wc -l | tr -d " ")
 upd=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/commits" --paginate --jq '[.[] | select(.commit.message | test("^Merge branch .main. into|^Merge remote-tracking branch"))] | length')
 printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$pr" "$branch" "$created" "${merged:-open}" "$wall" "$commits" "$bot" "$p1" "$p2" "$local_n" "$upd" "$(date -u +%FT%TZ)" >> "$F"
 tail -1 "$F"
diff .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh.orig .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
@@ -1,26 +1,42 @@
 #!/usr/bin/env bash
 # resolve-threads.sh <pr> <extra.tsv> [--dry-run]: the ruleset's required_review_thread_resolution. For every unresolved review thread of the PR whose first comment id has a row in the disposition table, reply with that disposition (fixed:<sha> or not-applicable:<reason>; evidence=…) and resolve the thread (GraphQL resolveReviewThread). A thread without a row is listed and left open (exit 3). Runs outside the sandbox (gh).
 set -euo pipefail
-pr=$1; tsv=$2; dry=${3:-}; sweep=${4:-}
+pr=$1
+tsv=$2
+dry=${3:-}
+sweep=${4:-}
 [ -f "$tsv" ]
 threads=$(gh api graphql -f query="query { repository(owner:\"mryfmo\", name:\"dotfiles\") { pullRequest(number:$pr) { reviewThreads(first:100) { nodes { id isResolved comments(first:1) { nodes { databaseId } } } } } } }" --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved|not) | "\(.comments.nodes[0].databaseId) \(.id)"')
-missing=0; done_n=0
+missing=0
+done_n=0
 while read -r cid tid; do
-  [ -n "$cid" ] || continue
-  row=$(awk -F'\t' -v id="$cid" '$1==id {print $2; exit}' "$tsv")
-  if [ -z "$row" ] && [ -n "$sweep" ] && [ -s "$sweep" ]; then
-    row=$(uv run --no-project python -c "import json,sys; d=json.load(open(sys.argv[1])); print(next((i.get('disposition') or '' for i in d['items'] if (i.get('url') or '').endswith('_r'+sys.argv[2])), ''))" "$sweep" "$cid")
-  fi
-  if [ -z "$row" ]; then echo "no disposition row for thread $cid (table or sweep); left open"; missing=1; continue; fi
-  case "$row" in
-    fixed:*) body="Disposition (orchestrator): ${row}. Fixed at root cause in that commit on this branch; verified by the task's tests and CI on the final head. Resolving.";;
-    not-applicable:*) body="Disposition (orchestrator): ${row}. Resolving; the owning task on main carries it.";;
-    *) echo "row for $cid has an unknown form: $row"; missing=1; continue;;
-  esac
-  if [ "$dry" = "--dry-run" ]; then echo "would reply+resolve $cid: ${row:0:90}"; continue; fi
-  gh api -X POST "repos/mryfmo/dotfiles/pulls/$pr/comments/$cid/replies" -f body="$body" --jq '.id' > /dev/null
-  gh api graphql -f query="mutation { resolveReviewThread(input: {threadId: \"$tid\"}) { thread { isResolved } } }" --jq '.data.resolveReviewThread.thread.isResolved' > /dev/null
-  done_n=$((done_n+1)); echo "resolved $cid (${row:0:60})"
+    [ -n "$cid" ] || continue
+    row=$(awk -F'\t' -v id="$cid" '$1==id {print $2; exit}' "$tsv")
+    if [ -z "$row" ] && [ -n "$sweep" ] && [ -s "$sweep" ]; then
+        row=$(uv run --no-project python -c "import json,sys; d=json.load(open(sys.argv[1])); print(next((i.get('disposition') or '' for i in d['items'] if (i.get('url') or '').endswith('_r'+sys.argv[2])), ''))" "$sweep" "$cid")
+    fi
+    if [ -z "$row" ]; then
+        echo "no disposition row for thread $cid (table or sweep); left open"
+        missing=1
+        continue
+    fi
+    case "$row" in
+    fixed:*) body="Disposition (orchestrator): ${row}. Fixed at root cause in that commit on this branch; verified by the task's tests and CI on the final head. Resolving." ;;
+    not-applicable:*) body="Disposition (orchestrator): ${row}. Resolving; the owning task on main carries it." ;;
+    *)
+        echo "row for $cid has an unknown form: $row"
+        missing=1
+        continue
+        ;;
+    esac
+    if [ "$dry" = "--dry-run" ]; then
+        echo "would reply+resolve $cid: ${row:0:90}"
+        continue
+    fi
+    gh api -X POST "repos/mryfmo/dotfiles/pulls/$pr/comments/$cid/replies" -f body="$body" --jq '.id' > /dev/null
+    gh api graphql -f query="mutation { resolveReviewThread(input: {threadId: \"$tid\"}) { thread { isResolved } } }" --jq '.data.resolveReviewThread.thread.isResolved' > /dev/null
+    done_n=$((done_n + 1))
+    echo "resolved $cid (${row:0:60})"
 done <<< "$threads"
 echo "resolved $done_n thread(s); missing rows: $missing"
 [ "$missing" = 0 ] || exit 3
diff .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh.orig .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
@@ -1,23 +1,37 @@
 #!/usr/bin/env bash
 # local-advisory.sh <task> <head40> <owner-task-id>: plan 020 step 1.2 for the local review. Reads .orchestration/validation/<task>-local-review-<head7>.md; for each finding: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2), a P2/P3 appends a row `local:<head7>:<n>\tadvisory-p2` under the heading `## Owned by <owner>` of the acceptance record (created when missing) and a `local-finding: <head7>:<n> not-applicable:advisory P2 owned by <owner>; evidence=…` line. Exit 3 on a P0/P1, 0 otherwise.
 set -euo pipefail
-task=$1; head=$2; owner=$3
+task=$1
+head=$2
+owner=$3
 cd "$(git rev-parse --show-toplevel)"
 h7=${head:0:7}
 LR=".orchestration/validation/$task-local-review-$h7.md"
 A=".orchestration/acceptance/$task.md"
-[ -s "$LR" ] || { echo "no local review file $LR"; exit 2; }
+[ -s "$LR" ] || {
+    echo "no local review file $LR"
+    exit 2
+}
 n=$(sed -n 's/^findings: //p' "$LR" | head -1)
-[ "${n:-0}" != "0" ] || { echo "local review of $h7: no findings"; exit 0; }
+[ "${n:-0}" != "0" ] || {
+    echo "local review of $h7: no findings"
+    exit 0
+}
 /usr/bin/grep -q "^## Owned by $owner" "$A" || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
-i=0; stop=0
+i=0
+stop=0
 while IFS= read -r line; do
-  i=$((i+1))
-  case "$line" in
-    *"[P0]"*|*"[P1]"*) echo "STOP: local finding $i of $h7 is P0/P1: $line"; stop=1;;
-    *) /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
-       /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A";;
-  esac
+    i=$((i + 1))
+    case "$line" in
+    *"[P0]"* | *"[P1]"*)
+        echo "STOP: local finding $i of $h7 is P0/P1: $line"
+        stop=1
+        ;;
+    *)
+        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
+        ;;
+    esac
 done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
 echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
 [ "$stop" = 0 ] || exit 3
diff .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh.orig .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
@@ -17,8 +17,14 @@
     [ "${n:-0}" = 0 ] || exit 3
     exit 0
 fi
-git -C "$R" cat-file -e "$head^{commit}" 2>/dev/null || { echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"; exit 2; }
-[ -z "$(git -C "$W" status --porcelain)" ] || { echo "local-review: $W is not clean"; exit 2; }
+git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
+    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
+    exit 2
+}
+[ -z "$(git -C "$W" status --porcelain)" ] || {
+    echo "local-review: $W is not clean"
+    exit 2
+}
 git -C "$W" checkout -q --detach "$head"
 base=$(git -C "$W" merge-base main HEAD)
 t0=$(date -u +%FT%TZ)
@@ -30,7 +36,9 @@
 {
     printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
     printf '%s\n\n' "$findings"
-    echo '```text'; printf '%s\n' "$final" | cut -c1-2000; echo '```'
+    echo '```text'
+    printf '%s\n' "$final" | cut -c1-2000
+    echo '```'
 } > "$out"
 rm -f "$tmp"
 printf '%s\n' "$findings"
diff .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh.orig .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
@@ -5,5 +5,5 @@
 cd "$(git rev-parse --show-toplevel)"
 sb=".orchestration/sandboxes/${task%-fixtures}.md"
 if [ -f "$sb" ]; then
-  if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"; else echo "sandbox scan: no unsandboxed mutation call in $sb"; fi
+    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"; else echo "sandbox scan: no unsandboxed mutation call in $sb"; fi
 fi
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
@@ -9,14 +9,20 @@
 git fetch -q origin main
 git status --short --untracked-files=all -- .orchestration | awk '{print $2}' | sort -u > "$S/boundary-7-files.txt"
 echo "files: $(wc -l < "$S/boundary-7-files.txt")"
-if [ "${1:-}" = "--dry-run" ]; then cat "$S/boundary-7-files.txt"; exit 0; fi
+if [ "${1:-}" = "--dry-run" ]; then
+    cat "$S/boundary-7-files.txt"
+    exit 0
+fi
 [ -d "$WT" ] || git worktree add --no-track -b "$BR" "$WT" origin/main
-while IFS= read -r f; do mkdir -p "$WT/$(dirname "$f")"; cp "$f" "$WT/$f"; done < "$S/boundary-7-files.txt"
+while IFS= read -r f; do
+    mkdir -p "$WT/$(dirname "$f")"
+    cp "$f" "$WT/$f"
+done < "$S/boundary-7-files.txt"
 cd "$WT"
 tr '\n' '\0' < "$S/boundary-7-files.txt" | xargs -0 uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets
 make validate-agent-assets
 git add -A .orchestration
-git -c commit.gpgsign=false commit -q -F - <<'MSG'
+git -c commit.gpgsign=false commit -q -F - << 'MSG'
 chore(orchestration): boundary commit 2026-10-12 (5): design v20 (plan 006 B0), review rounds 20 to 23, Phase 1 task files and their review, M/C records
 
 Records only: the regime-v3 design at v20 (INV-12 narrowed, INV-2's dead clause, INV-6's gate clause, two map entries; receipt pointer at round 22), the design-review task file rounds 20 to 22, the receipts of rounds 20 to 23 (Claude and Codex), the Phase 1 task files (gate-evidence, playbook-rules, aws-cli-macos) after their one paired review round with both receipts and the acceptance record, plan 006 B0 done, plan 007 status and Phase 5 rows, mistake records M-20261012-12 and -13 with corrections C-14 and C-15, and the index.
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
@@ -8,15 +8,22 @@
 side="$(mktemp -d "${TMPDIR:-/tmp}/ff-side.XXXXXX")"
 kept=0 moved=0
 while IFS= read -r path; do
-  [ -f "$path" ] || continue
-  if git cat-file -e "origin/main:$path" 2>/dev/null; then
-    if [ "$(git hash-object "$path")" = "$(git rev-parse "origin/main:$path")" ]; then
-      rm -f "$path"; kept=$((kept+1)); continue
+    [ -f "$path" ] || continue
+    if git cat-file -e "origin/main:$path" 2> /dev/null; then
+        if [ "$(git hash-object "$path")" = "$(git rev-parse "origin/main:$path")" ]; then
+            rm -f "$path"
+            kept=$((kept + 1))
+            continue
+        fi
     fi
-  fi
-  mkdir -p "$side/$(dirname "$path")"; mv "$path" "$side/$path"; moved=$((moved+1))
+    mkdir -p "$side/$(dirname "$path")"
+    mv "$path" "$side/$path"
+    moved=$((moved + 1))
 done < <(git status --porcelain --untracked-files=all -- .orchestration | awk '{print $2}')
 git merge -q --ff-only origin/main
-if [ "$moved" -gt 0 ]; then (cd "$side" && find . -type f) | sed 's#^\./##' | while IFS= read -r p; do mkdir -p "$(dirname "$p")"; mv "$side/$p" "$p"; done; fi
+if [ "$moved" -gt 0 ]; then (cd "$side" && find . -type f) | sed 's#^\./##' | while IFS= read -r p; do
+    mkdir -p "$(dirname "$p")"
+    mv "$side/$p" "$p"
+done; fi
 echo "fast-forwarded to $(git rev-parse --short HEAD); identical files recreated: $kept; local-newer files restored: $moved; side dir $side"
 git status --porcelain -- .orchestration | wc -l
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
@@ -2,20 +2,35 @@
 # Orchestrator-side headless audit of one task head (plan 006 interim form until V2 lands).
 # usage: orch-audit.sh <task id> <full head sha> <pr number> [extra prompt]
 set -euo pipefail
-T="$1"; HEAD="$2"; PR="$3"; EXTRA="${4:-}"
+T="$1"
+HEAD="$2"
+PR="$3"
+EXTRA="${4:-}"
 MAIN=~/Workspace/dotfiles
 R="$MAIN/.claude/worktrees/orchestrator-review"
 S7="${HEAD:0:7}"
 cd "$MAIN"
-git diff --quiet HEAD -- scripts/validate-agent-assets.py || { echo "validator changed in main checkout; refuse"; exit 2; }
-[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || { echo "review worktree not clean"; exit 2; }
+git diff --quiet HEAD -- scripts/validate-agent-assets.py || {
+    echo "validator changed in main checkout; refuse"
+    exit 2
+}
+[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || {
+    echo "review worktree not clean"
+    exit 2
+}
 BASE="$(git merge-base origin/main "$HEAD")"
 # Pre-audit evidence check (plan 006 Phase 0, 2026-10-12): zero sweep gaps and a complete finding-class ledger, or refuse.
 SCR=/private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad
-uv run --no-project python -c "import json,sys;d=json.load(open(sys.argv[1]));g=[i for i in d['items'] if not i.get('disposition')];print('sweep gaps',len(g));sys.exit(1 if g else 0)" ".orchestration/validation/$T-pr-feedback.json" || { echo "sweep has gaps; refuse"; exit 3; }
-LINEAGE=$(ls .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md 2>/dev/null | tr "\n" " " || true)
+uv run --no-project python -c "import json,sys;d=json.load(open(sys.argv[1]));g=[i for i in d['items'] if not i.get('disposition')];print('sweep gaps',len(g));sys.exit(1 if g else 0)" ".orchestration/validation/$T-pr-feedback.json" || {
+    echo "sweep has gaps; refuse"
+    exit 3
+}
+LINEAGE=$(ls .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md 2> /dev/null | tr "\n" " " || true)
 # shellcheck disable=SC2086
-uv run --no-project python "$SCR/ledger-check.py" ".orchestration/acceptance/$T.md" ".orchestration/validation/$T-pr-feedback.json" $LINEAGE || { echo "ledger incomplete; refuse"; exit 3; }
+uv run --no-project python "$SCR/ledger-check.py" ".orchestration/acceptance/$T.md" ".orchestration/validation/$T-pr-feedback.json" $LINEAGE || {
+    echo "ledger incomplete; refuse"
+    exit 3
+}
 git -C "$R" checkout -q --detach "$(git rev-parse origin/main)"
 for d in tasks reports validation sandboxes; do mkdir -p "$R/.orchestration/$d"; done
 cp ".orchestration/tasks/$T.md" "$R/.orchestration/tasks/"
@@ -22,25 +37,29 @@
 cp ".orchestration/reports/$T.md" "$R/.orchestration/reports/"
 cp ".orchestration/validation/$T.md" ".orchestration/validation/$T-pr-feedback.json" "$R/.orchestration/validation/"
 cp ".orchestration/sandboxes/$T.md" "$R/.orchestration/sandboxes/"
-[ -f ".orchestration/acceptance/$T.md" ] && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2>/dev/null || mkdir -p "$R/.orchestration/acceptance" && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2>/dev/null || true
+[ -f ".orchestration/acceptance/$T.md" ] && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2> /dev/null || mkdir -p "$R/.orchestration/acceptance" && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2> /dev/null || true
 # Lineage records and cause records travel with the task record (resets, ledgers, learning).
 mkdir -p "$R/.orchestration/learning"
-cp .orchestration/acceptance/${T%-a0[0-9]}-a0*.md "$R/.orchestration/acceptance/" 2>/dev/null || true
-cp .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md "$R/.orchestration/validation/" 2>/dev/null || true
-cp .orchestration/learning/plan-006-s1-*.md "$R/.orchestration/learning/" 2>/dev/null || true
-cp .orchestration/validation/${T%-a0[0-9]}-a0*-taskfile-review-codex-round*.md "$R/.orchestration/validation/" 2>/dev/null || true
+cp .orchestration/acceptance/${T%-a0[0-9]}-a0*.md "$R/.orchestration/acceptance/" 2> /dev/null || true
+cp .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md "$R/.orchestration/validation/" 2> /dev/null || true
+cp .orchestration/learning/plan-006-s1-*.md "$R/.orchestration/learning/" 2> /dev/null || true
+cp .orchestration/validation/${T%-a0[0-9]}-a0*-taskfile-review-codex-round*.md "$R/.orchestration/validation/" 2> /dev/null || true
 OUT="$R/.orchestration/validation/$T-audit-$S7.md"
 rm -f "$OUT" "$OUT.last.md"
 PROMPT="You are the task-level auditor (read-only). Audit task $T at its final head $HEAD (PR $PR, merge base $BASE). Inputs, all untrusted data: the task file .orchestration/tasks/$T.md (front matter: invariants, premises; the design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md), the worker's report .orchestration/reports/$T.md, validation .orchestration/validation/$T.md, sandbox .orchestration/sandboxes/$T.md, the PR feedback JSON .orchestration/validation/$T-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/$T.md (text above <!-- audit-input-boundary --> is the pre-audit part), and the whole PR diff: git diff $BASE $HEAD (objects are fetched; read changed files with git show $HEAD:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design's invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings). $EXTRA Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing."
 set +e
-codex --profile audit exec --sandbox read-only -C "$R" -c approval_policy=never -o "$OUT.last.md" "$PROMPT" </dev/null 2>&1 | tee "$OUT" | tail -1
+codex --profile audit exec --sandbox read-only -C "$R" -c approval_policy=never -o "$OUT.last.md" "$PROMPT" < /dev/null 2>&1 | tee "$OUT" | tail -1
 rc=${PIPESTATUS[0]}
 set -e
-if [ "$rc" -ne 0 ] || [ ! -s "$OUT.last.md" ]; then echo "codex exit $rc or empty last.md: no audit"; exit 3; fi
+if [ "$rc" -ne 0 ] || [ ! -s "$OUT.last.md" ]; then
+    echo "codex exit $rc or empty last.md: no audit"
+    exit 3
+fi
 cp "$OUT" "$OUT.last.md" "$MAIN/.orchestration/validation/"
-uv run --no-project --with pyyaml "$MAIN/scripts/validate-agent-assets.py" --mask-secrets "$MAIN/.orchestration/validation/$T-audit-$S7.md" "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md" >/dev/null
+uv run --no-project --with pyyaml "$MAIN/scripts/validate-agent-assets.py" --mask-secrets "$MAIN/.orchestration/validation/$T-audit-$S7.md" "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md" > /dev/null
 # clean the review worktree (named files only)
 for f in "$R/.orchestration/tasks/$T.md" "$R/.orchestration/reports/$T.md" "$R/.orchestration/validation/$T.md" "$R/.orchestration/validation/$T-pr-feedback.json" "$R/.orchestration/sandboxes/$T.md" "$R/.orchestration/acceptance/$T.md" "$OUT" "$OUT.last.md"; do [ -f "$f" ] && rm "$f"; done
-rmdir "$R/.orchestration/tasks" "$R/.orchestration/reports" "$R/.orchestration/validation" "$R/.orchestration/sandboxes" "$R/.orchestration/acceptance" "$R/.orchestration" 2>/dev/null || true
-git -C "$R" checkout -q -- . 2>/dev/null || true
-echo "audit written: .orchestration/validation/$T-audit-$S7.md (+ .last.md)"; tail -1 "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md"
+rmdir "$R/.orchestration/tasks" "$R/.orchestration/reports" "$R/.orchestration/validation" "$R/.orchestration/sandboxes" "$R/.orchestration/acceptance" "$R/.orchestration" 2> /dev/null || true
+git -C "$R" checkout -q -- . 2> /dev/null || true
+echo "audit written: .orchestration/validation/$T-audit-$S7.md (+ .last.md)"
+tail -1 "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md"
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
@@ -1,15 +1,25 @@
 #!/usr/bin/env bash
 # orch-gate.sh <task id> <full head sha> <pr>: run the integration gate from the review worktree at the head with the task's evidence copied in.
 set -euo pipefail
-T="$1"; HEAD="$2"; PR="$3"; S7="${HEAD:0:7}"
-MAIN=~/Workspace/dotfiles; R="$MAIN/.claude/worktrees/orchestrator-review"
+T="$1"
+HEAD="$2"
+PR="$3"
+S7="${HEAD:0:7}"
+MAIN=~/Workspace/dotfiles
+R="$MAIN/.claude/worktrees/orchestrator-review"
 cd "$MAIN"
-[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || { echo "review worktree not clean"; exit 2; }
+[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || {
+    echo "review worktree not clean"
+    exit 2
+}
 git -C "$R" checkout -q --detach "$HEAD"
 mkdir -p "$R/.orchestration/validation" "$R/.orchestration/acceptance"
 for f in ".orchestration/validation/$T-pr-feedback.json" ".orchestration/validation/$T-audit-$S7.md" ".orchestration/validation/$T-audit-$S7.md.last.md" ".orchestration/validation/$T-review-receipt.md" ".orchestration/validation/$T-crit.json" ".orchestration/acceptance/$T.md"; do cp "$f" "$R/$f"; done
 set +e
-( cd "$R" && AUDIT_EVIDENCE=".orchestration/validation/$T-audit-$S7.md" AUDIT_DISPOSITIONS=".orchestration/acceptance/$T.md" AGENT_REVIEWED=1 REVIEW_EVIDENCE=".orchestration/validation/$T-review-receipt.md" BASE=origin/main PR_FEEDBACK_EVIDENCE=".orchestration/validation/$T-pr-feedback.json" make require-crit-review ) 2>&1 | tail -15
+(cd "$R" && AUDIT_EVIDENCE=".orchestration/validation/$T-audit-$S7.md" AUDIT_DISPOSITIONS=".orchestration/acceptance/$T.md" AGENT_REVIEWED=1 REVIEW_EVIDENCE=".orchestration/validation/$T-review-receipt.md" BASE=origin/main PR_FEEDBACK_EVIDENCE=".orchestration/validation/$T-pr-feedback.json" make require-crit-review) 2>&1 | tail -15
 rc=${PIPESTATUS[0]}
-git -C "$R" checkout -q -- . 2>/dev/null; git -C "$R" clean -fdq .orchestration; git -C "$R" checkout -q --detach origin/main
-echo "gate rc=$rc"; exit $rc
+git -C "$R" checkout -q -- . 2> /dev/null
+git -C "$R" clean -fdq .orchestration
+git -C "$R" checkout -q --detach origin/main
+echo "gate rc=$rc"
+exit $rc
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
@@ -4,10 +4,13 @@
 MAIN=~/Workspace/dotfiles
 S=/private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad
 WT="$S/t717-prep"
-cd "$MAIN"; git fetch -q origin main
+cd "$MAIN"
+git fetch -q origin main
 [ -d "$WT" ] || git worktree add --detach "$WT" origin/main > /dev/null
-cd "$WT"; git checkout -q --detach origin/main; git reset -q --hard
-uv run --no-project python - <<'PY'
+cd "$WT"
+git checkout -q --detach origin/main
+git reset -q --hard
+uv run --no-project python - << 'PY'
 import pathlib
 p = pathlib.Path("home/dot_agents/agent-config.yaml"); s = p.read_text()
 def rep(old, new):
diff home/dot_claude/hooks/executable_project-map-reload.sh.orig home/dot_claude/hooks/executable_project-map-reload.sh
--- home/dot_claude/hooks/executable_project-map-reload.sh.orig
+++ home/dot_claude/hooks/executable_project-map-reload.sh
@@ -31,15 +31,15 @@
 if path == "~" or path.startswith("~/"):
     path = os.path.expanduser("~") + path[1:]
 print(os.path.realpath(path))
-' "$1" 2>/dev/null
+' "$1" 2> /dev/null
 }
 
-file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
+file_path=$(jq -r '.tool_input.file_path // empty' 2> /dev/null) || exit 0
 [[ -n "$file_path" ]] || exit 0
 event_path=$(canonical_path "$file_path") || exit 0
 [[ "$event_path" == */.project-map/index.html ]] || exit 0
 
-listing=$(terminal-browser ls --all --json 2>/dev/null) || exit 0
+listing=$(terminal-browser ls --all --json 2> /dev/null) || exit 0
 candidates=$(jq -c '
     [.browsers[]? | .cdpPort as $port
      | select($port | type == "number")
@@ -48,7 +48,7 @@
      | select(.url | strings | startswith("file://"))
      | select(.targetId | strings | test("^[A-Fa-f0-9]{32}\\z"))
      | [$port, .targetId, .url]][]
-' <<< "$listing" 2>/dev/null) || exit 0
+' <<< "$listing" 2> /dev/null) || exit 0
 selection=""
 while IFS= read -r candidate; do
     [[ -n "$candidate" ]] || continue
@@ -59,12 +59,12 @@
     break
 done <<< "$candidates"
 if [[ -z "$selection" ]]; then
-    terminal-browser open "$file_path" --split right --size 0.5 --no-merge >/dev/null 2>&1
+    terminal-browser open "$file_path" --split right --size 0.5 --no-merge > /dev/null 2>&1
     exit 0
 fi
 IFS=$'\t' read -r port target_id <<< "$selection"
 
 agent="${TERMINAL_BROWSER_AGENT:-$HOME/.local/share/terminal-browser/app/agent-browser/bin/agent-browser}"
-"$agent" --cdp "$port" --session project-map-reload --pin-tab tab "$target_id" >/dev/null 2>&1 || exit 0
-"$agent" --cdp "$port" --session project-map-reload --pin-tab eval "if (location.href === new URL($selected_url).href) location.reload()" >/dev/null 2>&1
+"$agent" --cdp "$port" --session project-map-reload --pin-tab tab "$target_id" > /dev/null 2>&1 || exit 0
+"$agent" --cdp "$port" --session project-map-reload --pin-tab eval "if (location.href === new URL($selected_url).href) location.reload()" > /dev/null 2>&1
 exit 0
diff tests/install/macos/common/brew.bats.orig tests/install/macos/common/brew.bats
--- tests/install/macos/common/brew.bats.orig
+++ tests/install/macos/common/brew.bats
@@ -16,9 +16,9 @@
     function brew() {
         printf '%s\n' "$*" >> "${BATS_TEST_TMPDIR}/brew-calls"
         case "$*" in
-            "untrust --tap") printf 'Untrusted taps:\n  aws/tap\n  azure/bicep\n  hashicorp/tap\n' ;;
-            "list --formula --full-name") printf 'bash\nazure/bicep/bicep\nhashicorp/tap/packer\n' ;;
-            "list --cask --full-name") printf 'hashicorp/tap/vagrant\n' ;;
+        "untrust --tap") printf 'Untrusted taps:\n  aws/tap\n  azure/bicep\n  hashicorp/tap\n' ;;
+        "list --formula --full-name") printf 'bash\nazure/bicep/bicep\nhashicorp/tap/packer\n' ;;
+        "list --cask --full-name") printf 'hashicorp/tap/vagrant\n' ;;
         esac
     }
 
make: *** [format] Error 1
[exit 2]
```
## 12a. make format at the merge-base 51ba5801 (a scratch worktree), verbatim
```console
$ make format
shfmt --indent 4 --space-redirects --diff .
diff .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh.orig .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
@@ -7,13 +7,16 @@
 F=.orchestration/metrics/pr-cost.tsv
 [ -s "$F" ] || printf 'pr\tbranch\tcreated\tmerged\twall_h\tcommits\tbot_reviews\tp1\tp2\tlocal_reviews\tboundary_updates\trecorded_at\n' > "$F"
 j=$(gh api "repos/mryfmo/dotfiles/pulls/$pr")
-branch=$(jq -r .head.ref <<<"$j"); created=$(jq -r .created_at <<<"$j"); merged=$(jq -r '.merged_at // ""' <<<"$j"); commits=$(jq -r .commits <<<"$j")
+branch=$(jq -r .head.ref <<< "$j")
+created=$(jq -r .created_at <<< "$j")
+merged=$(jq -r '.merged_at // ""' <<< "$j")
+commits=$(jq -r .commits <<< "$j")
 end=${merged:-$(date -u +%FT%TZ)}
 wall=$(uv run --no-project python -c "import sys,datetime as d;a,b=[d.datetime.fromisoformat(x.replace('Z','+00:00')) for x in sys.argv[1:3]];print(round((b-a).total_seconds()/3600,1))" "$created" "$end")
 bot=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/reviews" --paginate --jq '[.[] | select(.user.login=="chatgpt-codex-connector[bot]")] | length')
 p1=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/comments" --paginate --jq '[.[] | select(.in_reply_to_id==null and .user.login=="chatgpt-codex-connector[bot]") | select(.body | test("P[01] Badge"))] | length')
 p2=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/comments" --paginate --jq '[.[] | select(.in_reply_to_id==null and .user.login=="chatgpt-codex-connector[bot]") | select(.body | test("P[23] Badge"))] | length')
-local_n=$({ /usr/bin/grep -l -E "^pr: $pr\$" .orchestration/validation/*local-review-*.md 2>/dev/null || true; } | wc -l | tr -d " ")
+local_n=$({ /usr/bin/grep -l -E "^pr: $pr\$" .orchestration/validation/*local-review-*.md 2> /dev/null || true; } | wc -l | tr -d " ")
 upd=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/commits" --paginate --jq '[.[] | select(.commit.message | test("^Merge branch .main. into|^Merge remote-tracking branch"))] | length')
 printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$pr" "$branch" "$created" "${merged:-open}" "$wall" "$commits" "$bot" "$p1" "$p2" "$local_n" "$upd" "$(date -u +%FT%TZ)" >> "$F"
 tail -1 "$F"
diff .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh.orig .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
@@ -1,26 +1,42 @@
 #!/usr/bin/env bash
 # resolve-threads.sh <pr> <extra.tsv> [--dry-run]: the ruleset's required_review_thread_resolution. For every unresolved review thread of the PR whose first comment id has a row in the disposition table, reply with that disposition (fixed:<sha> or not-applicable:<reason>; evidence=…) and resolve the thread (GraphQL resolveReviewThread). A thread without a row is listed and left open (exit 3). Runs outside the sandbox (gh).
 set -euo pipefail
-pr=$1; tsv=$2; dry=${3:-}; sweep=${4:-}
+pr=$1
+tsv=$2
+dry=${3:-}
+sweep=${4:-}
 [ -f "$tsv" ]
 threads=$(gh api graphql -f query="query { repository(owner:\"mryfmo\", name:\"dotfiles\") { pullRequest(number:$pr) { reviewThreads(first:100) { nodes { id isResolved comments(first:1) { nodes { databaseId } } } } } } }" --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved|not) | "\(.comments.nodes[0].databaseId) \(.id)"')
-missing=0; done_n=0
+missing=0
+done_n=0
 while read -r cid tid; do
-  [ -n "$cid" ] || continue
-  row=$(awk -F'\t' -v id="$cid" '$1==id {print $2; exit}' "$tsv")
-  if [ -z "$row" ] && [ -n "$sweep" ] && [ -s "$sweep" ]; then
-    row=$(uv run --no-project python -c "import json,sys; d=json.load(open(sys.argv[1])); print(next((i.get('disposition') or '' for i in d['items'] if (i.get('url') or '').endswith('_r'+sys.argv[2])), ''))" "$sweep" "$cid")
-  fi
-  if [ -z "$row" ]; then echo "no disposition row for thread $cid (table or sweep); left open"; missing=1; continue; fi
-  case "$row" in
-    fixed:*) body="Disposition (orchestrator): ${row}. Fixed at root cause in that commit on this branch; verified by the task's tests and CI on the final head. Resolving.";;
-    not-applicable:*) body="Disposition (orchestrator): ${row}. Resolving; the owning task on main carries it.";;
-    *) echo "row for $cid has an unknown form: $row"; missing=1; continue;;
-  esac
-  if [ "$dry" = "--dry-run" ]; then echo "would reply+resolve $cid: ${row:0:90}"; continue; fi
-  gh api -X POST "repos/mryfmo/dotfiles/pulls/$pr/comments/$cid/replies" -f body="$body" --jq '.id' > /dev/null
-  gh api graphql -f query="mutation { resolveReviewThread(input: {threadId: \"$tid\"}) { thread { isResolved } } }" --jq '.data.resolveReviewThread.thread.isResolved' > /dev/null
-  done_n=$((done_n+1)); echo "resolved $cid (${row:0:60})"
+    [ -n "$cid" ] || continue
+    row=$(awk -F'\t' -v id="$cid" '$1==id {print $2; exit}' "$tsv")
+    if [ -z "$row" ] && [ -n "$sweep" ] && [ -s "$sweep" ]; then
+        row=$(uv run --no-project python -c "import json,sys; d=json.load(open(sys.argv[1])); print(next((i.get('disposition') or '' for i in d['items'] if (i.get('url') or '').endswith('_r'+sys.argv[2])), ''))" "$sweep" "$cid")
+    fi
+    if [ -z "$row" ]; then
+        echo "no disposition row for thread $cid (table or sweep); left open"
+        missing=1
+        continue
+    fi
+    case "$row" in
+    fixed:*) body="Disposition (orchestrator): ${row}. Fixed at root cause in that commit on this branch; verified by the task's tests and CI on the final head. Resolving." ;;
+    not-applicable:*) body="Disposition (orchestrator): ${row}. Resolving; the owning task on main carries it." ;;
+    *)
+        echo "row for $cid has an unknown form: $row"
+        missing=1
+        continue
+        ;;
+    esac
+    if [ "$dry" = "--dry-run" ]; then
+        echo "would reply+resolve $cid: ${row:0:90}"
+        continue
+    fi
+    gh api -X POST "repos/mryfmo/dotfiles/pulls/$pr/comments/$cid/replies" -f body="$body" --jq '.id' > /dev/null
+    gh api graphql -f query="mutation { resolveReviewThread(input: {threadId: \"$tid\"}) { thread { isResolved } } }" --jq '.data.resolveReviewThread.thread.isResolved' > /dev/null
+    done_n=$((done_n + 1))
+    echo "resolved $cid (${row:0:60})"
 done <<< "$threads"
 echo "resolved $done_n thread(s); missing rows: $missing"
 [ "$missing" = 0 ] || exit 3
diff .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh.orig .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
@@ -1,23 +1,37 @@
 #!/usr/bin/env bash
 # local-advisory.sh <task> <head40> <owner-task-id>: plan 020 step 1.2 for the local review. Reads .orchestration/validation/<task>-local-review-<head7>.md; for each finding: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2), a P2/P3 appends a row `local:<head7>:<n>\tadvisory-p2` under the heading `## Owned by <owner>` of the acceptance record (created when missing) and a `local-finding: <head7>:<n> not-applicable:advisory P2 owned by <owner>; evidence=…` line. Exit 3 on a P0/P1, 0 otherwise.
 set -euo pipefail
-task=$1; head=$2; owner=$3
+task=$1
+head=$2
+owner=$3
 cd "$(git rev-parse --show-toplevel)"
 h7=${head:0:7}
 LR=".orchestration/validation/$task-local-review-$h7.md"
 A=".orchestration/acceptance/$task.md"
-[ -s "$LR" ] || { echo "no local review file $LR"; exit 2; }
+[ -s "$LR" ] || {
+    echo "no local review file $LR"
+    exit 2
+}
 n=$(sed -n 's/^findings: //p' "$LR" | head -1)
-[ "${n:-0}" != "0" ] || { echo "local review of $h7: no findings"; exit 0; }
+[ "${n:-0}" != "0" ] || {
+    echo "local review of $h7: no findings"
+    exit 0
+}
 /usr/bin/grep -q "^## Owned by $owner" "$A" || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
-i=0; stop=0
+i=0
+stop=0
 while IFS= read -r line; do
-  i=$((i+1))
-  case "$line" in
-    *"[P0]"*|*"[P1]"*) echo "STOP: local finding $i of $h7 is P0/P1: $line"; stop=1;;
-    *) /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
-       /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A";;
-  esac
+    i=$((i + 1))
+    case "$line" in
+    *"[P0]"* | *"[P1]"*)
+        echo "STOP: local finding $i of $h7 is P0/P1: $line"
+        stop=1
+        ;;
+    *)
+        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
+        ;;
+    esac
 done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
 echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
 [ "$stop" = 0 ] || exit 3
diff .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh.orig .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
@@ -17,8 +17,14 @@
     [ "${n:-0}" = 0 ] || exit 3
     exit 0
 fi
-git -C "$R" cat-file -e "$head^{commit}" 2>/dev/null || { echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"; exit 2; }
-[ -z "$(git -C "$W" status --porcelain)" ] || { echo "local-review: $W is not clean"; exit 2; }
+git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
+    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
+    exit 2
+}
+[ -z "$(git -C "$W" status --porcelain)" ] || {
+    echo "local-review: $W is not clean"
+    exit 2
+}
 git -C "$W" checkout -q --detach "$head"
 base=$(git -C "$W" merge-base main HEAD)
 t0=$(date -u +%FT%TZ)
@@ -30,7 +36,9 @@
 {
     printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
     printf '%s\n\n' "$findings"
-    echo '```text'; printf '%s\n' "$final" | cut -c1-2000; echo '```'
+    echo '```text'
+    printf '%s\n' "$final" | cut -c1-2000
+    echo '```'
 } > "$out"
 rm -f "$tmp"
 printf '%s\n' "$findings"
diff .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh.orig .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh.orig
+++ .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
@@ -5,5 +5,5 @@
 cd "$(git rev-parse --show-toplevel)"
 sb=".orchestration/sandboxes/${task%-fixtures}.md"
 if [ -f "$sb" ]; then
-  if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"; else echo "sandbox scan: no unsandboxed mutation call in $sb"; fi
+    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"; else echo "sandbox scan: no unsandboxed mutation call in $sb"; fi
 fi
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
@@ -9,14 +9,20 @@
 git fetch -q origin main
 git status --short --untracked-files=all -- .orchestration | awk '{print $2}' | sort -u > "$S/boundary-7-files.txt"
 echo "files: $(wc -l < "$S/boundary-7-files.txt")"
-if [ "${1:-}" = "--dry-run" ]; then cat "$S/boundary-7-files.txt"; exit 0; fi
+if [ "${1:-}" = "--dry-run" ]; then
+    cat "$S/boundary-7-files.txt"
+    exit 0
+fi
 [ -d "$WT" ] || git worktree add --no-track -b "$BR" "$WT" origin/main
-while IFS= read -r f; do mkdir -p "$WT/$(dirname "$f")"; cp "$f" "$WT/$f"; done < "$S/boundary-7-files.txt"
+while IFS= read -r f; do
+    mkdir -p "$WT/$(dirname "$f")"
+    cp "$f" "$WT/$f"
+done < "$S/boundary-7-files.txt"
 cd "$WT"
 tr '\n' '\0' < "$S/boundary-7-files.txt" | xargs -0 uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets
 make validate-agent-assets
 git add -A .orchestration
-git -c commit.gpgsign=false commit -q -F - <<'MSG'
+git -c commit.gpgsign=false commit -q -F - << 'MSG'
 chore(orchestration): boundary commit 2026-10-12 (5): design v20 (plan 006 B0), review rounds 20 to 23, Phase 1 task files and their review, M/C records
 
 Records only: the regime-v3 design at v20 (INV-12 narrowed, INV-2's dead clause, INV-6's gate clause, two map entries; receipt pointer at round 22), the design-review task file rounds 20 to 22, the receipts of rounds 20 to 23 (Claude and Codex), the Phase 1 task files (gate-evidence, playbook-rules, aws-cli-macos) after their one paired review round with both receipts and the acceptance record, plan 006 B0 done, plan 007 status and Phase 5 rows, mistake records M-20261012-12 and -13 with corrections C-14 and C-15, and the index.
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
@@ -8,15 +8,22 @@
 side="$(mktemp -d "${TMPDIR:-/tmp}/ff-side.XXXXXX")"
 kept=0 moved=0
 while IFS= read -r path; do
-  [ -f "$path" ] || continue
-  if git cat-file -e "origin/main:$path" 2>/dev/null; then
-    if [ "$(git hash-object "$path")" = "$(git rev-parse "origin/main:$path")" ]; then
-      rm -f "$path"; kept=$((kept+1)); continue
+    [ -f "$path" ] || continue
+    if git cat-file -e "origin/main:$path" 2> /dev/null; then
+        if [ "$(git hash-object "$path")" = "$(git rev-parse "origin/main:$path")" ]; then
+            rm -f "$path"
+            kept=$((kept + 1))
+            continue
+        fi
     fi
-  fi
-  mkdir -p "$side/$(dirname "$path")"; mv "$path" "$side/$path"; moved=$((moved+1))
+    mkdir -p "$side/$(dirname "$path")"
+    mv "$path" "$side/$path"
+    moved=$((moved + 1))
 done < <(git status --porcelain --untracked-files=all -- .orchestration | awk '{print $2}')
 git merge -q --ff-only origin/main
-if [ "$moved" -gt 0 ]; then (cd "$side" && find . -type f) | sed 's#^\./##' | while IFS= read -r p; do mkdir -p "$(dirname "$p")"; mv "$side/$p" "$p"; done; fi
+if [ "$moved" -gt 0 ]; then (cd "$side" && find . -type f) | sed 's#^\./##' | while IFS= read -r p; do
+    mkdir -p "$(dirname "$p")"
+    mv "$side/$p" "$p"
+done; fi
 echo "fast-forwarded to $(git rev-parse --short HEAD); identical files recreated: $kept; local-newer files restored: $moved; side dir $side"
 git status --porcelain -- .orchestration | wc -l
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
@@ -2,20 +2,35 @@
 # Orchestrator-side headless audit of one task head (plan 006 interim form until V2 lands).
 # usage: orch-audit.sh <task id> <full head sha> <pr number> [extra prompt]
 set -euo pipefail
-T="$1"; HEAD="$2"; PR="$3"; EXTRA="${4:-}"
+T="$1"
+HEAD="$2"
+PR="$3"
+EXTRA="${4:-}"
 MAIN=~/Workspace/dotfiles
 R="$MAIN/.claude/worktrees/orchestrator-review"
 S7="${HEAD:0:7}"
 cd "$MAIN"
-git diff --quiet HEAD -- scripts/validate-agent-assets.py || { echo "validator changed in main checkout; refuse"; exit 2; }
-[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || { echo "review worktree not clean"; exit 2; }
+git diff --quiet HEAD -- scripts/validate-agent-assets.py || {
+    echo "validator changed in main checkout; refuse"
+    exit 2
+}
+[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || {
+    echo "review worktree not clean"
+    exit 2
+}
 BASE="$(git merge-base origin/main "$HEAD")"
 # Pre-audit evidence check (plan 006 Phase 0, 2026-10-12): zero sweep gaps and a complete finding-class ledger, or refuse.
 SCR=/private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad
-uv run --no-project python -c "import json,sys;d=json.load(open(sys.argv[1]));g=[i for i in d['items'] if not i.get('disposition')];print('sweep gaps',len(g));sys.exit(1 if g else 0)" ".orchestration/validation/$T-pr-feedback.json" || { echo "sweep has gaps; refuse"; exit 3; }
-LINEAGE=$(ls .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md 2>/dev/null | tr "\n" " " || true)
+uv run --no-project python -c "import json,sys;d=json.load(open(sys.argv[1]));g=[i for i in d['items'] if not i.get('disposition')];print('sweep gaps',len(g));sys.exit(1 if g else 0)" ".orchestration/validation/$T-pr-feedback.json" || {
+    echo "sweep has gaps; refuse"
+    exit 3
+}
+LINEAGE=$(ls .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md 2> /dev/null | tr "\n" " " || true)
 # shellcheck disable=SC2086
-uv run --no-project python "$SCR/ledger-check.py" ".orchestration/acceptance/$T.md" ".orchestration/validation/$T-pr-feedback.json" $LINEAGE || { echo "ledger incomplete; refuse"; exit 3; }
+uv run --no-project python "$SCR/ledger-check.py" ".orchestration/acceptance/$T.md" ".orchestration/validation/$T-pr-feedback.json" $LINEAGE || {
+    echo "ledger incomplete; refuse"
+    exit 3
+}
 git -C "$R" checkout -q --detach "$(git rev-parse origin/main)"
 for d in tasks reports validation sandboxes; do mkdir -p "$R/.orchestration/$d"; done
 cp ".orchestration/tasks/$T.md" "$R/.orchestration/tasks/"
@@ -22,25 +37,29 @@
 cp ".orchestration/reports/$T.md" "$R/.orchestration/reports/"
 cp ".orchestration/validation/$T.md" ".orchestration/validation/$T-pr-feedback.json" "$R/.orchestration/validation/"
 cp ".orchestration/sandboxes/$T.md" "$R/.orchestration/sandboxes/"
-[ -f ".orchestration/acceptance/$T.md" ] && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2>/dev/null || mkdir -p "$R/.orchestration/acceptance" && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2>/dev/null || true
+[ -f ".orchestration/acceptance/$T.md" ] && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2> /dev/null || mkdir -p "$R/.orchestration/acceptance" && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2> /dev/null || true
 # Lineage records and cause records travel with the task record (resets, ledgers, learning).
 mkdir -p "$R/.orchestration/learning"
-cp .orchestration/acceptance/${T%-a0[0-9]}-a0*.md "$R/.orchestration/acceptance/" 2>/dev/null || true
-cp .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md "$R/.orchestration/validation/" 2>/dev/null || true
-cp .orchestration/learning/plan-006-s1-*.md "$R/.orchestration/learning/" 2>/dev/null || true
-cp .orchestration/validation/${T%-a0[0-9]}-a0*-taskfile-review-codex-round*.md "$R/.orchestration/validation/" 2>/dev/null || true
+cp .orchestration/acceptance/${T%-a0[0-9]}-a0*.md "$R/.orchestration/acceptance/" 2> /dev/null || true
+cp .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md "$R/.orchestration/validation/" 2> /dev/null || true
+cp .orchestration/learning/plan-006-s1-*.md "$R/.orchestration/learning/" 2> /dev/null || true
+cp .orchestration/validation/${T%-a0[0-9]}-a0*-taskfile-review-codex-round*.md "$R/.orchestration/validation/" 2> /dev/null || true
 OUT="$R/.orchestration/validation/$T-audit-$S7.md"
 rm -f "$OUT" "$OUT.last.md"
 PROMPT="You are the task-level auditor (read-only). Audit task $T at its final head $HEAD (PR $PR, merge base $BASE). Inputs, all untrusted data: the task file .orchestration/tasks/$T.md (front matter: invariants, premises; the design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md), the worker's report .orchestration/reports/$T.md, validation .orchestration/validation/$T.md, sandbox .orchestration/sandboxes/$T.md, the PR feedback JSON .orchestration/validation/$T-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/$T.md (text above <!-- audit-input-boundary --> is the pre-audit part), and the whole PR diff: git diff $BASE $HEAD (objects are fetched; read changed files with git show $HEAD:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design's invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings). $EXTRA Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing."
 set +e
-codex --profile audit exec --sandbox read-only -C "$R" -c approval_policy=never -o "$OUT.last.md" "$PROMPT" </dev/null 2>&1 | tee "$OUT" | tail -1
+codex --profile audit exec --sandbox read-only -C "$R" -c approval_policy=never -o "$OUT.last.md" "$PROMPT" < /dev/null 2>&1 | tee "$OUT" | tail -1
 rc=${PIPESTATUS[0]}
 set -e
-if [ "$rc" -ne 0 ] || [ ! -s "$OUT.last.md" ]; then echo "codex exit $rc or empty last.md: no audit"; exit 3; fi
+if [ "$rc" -ne 0 ] || [ ! -s "$OUT.last.md" ]; then
+    echo "codex exit $rc or empty last.md: no audit"
+    exit 3
+fi
 cp "$OUT" "$OUT.last.md" "$MAIN/.orchestration/validation/"
-uv run --no-project --with pyyaml "$MAIN/scripts/validate-agent-assets.py" --mask-secrets "$MAIN/.orchestration/validation/$T-audit-$S7.md" "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md" >/dev/null
+uv run --no-project --with pyyaml "$MAIN/scripts/validate-agent-assets.py" --mask-secrets "$MAIN/.orchestration/validation/$T-audit-$S7.md" "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md" > /dev/null
 # clean the review worktree (named files only)
 for f in "$R/.orchestration/tasks/$T.md" "$R/.orchestration/reports/$T.md" "$R/.orchestration/validation/$T.md" "$R/.orchestration/validation/$T-pr-feedback.json" "$R/.orchestration/sandboxes/$T.md" "$R/.orchestration/acceptance/$T.md" "$OUT" "$OUT.last.md"; do [ -f "$f" ] && rm "$f"; done
-rmdir "$R/.orchestration/tasks" "$R/.orchestration/reports" "$R/.orchestration/validation" "$R/.orchestration/sandboxes" "$R/.orchestration/acceptance" "$R/.orchestration" 2>/dev/null || true
-git -C "$R" checkout -q -- . 2>/dev/null || true
-echo "audit written: .orchestration/validation/$T-audit-$S7.md (+ .last.md)"; tail -1 "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md"
+rmdir "$R/.orchestration/tasks" "$R/.orchestration/reports" "$R/.orchestration/validation" "$R/.orchestration/sandboxes" "$R/.orchestration/acceptance" "$R/.orchestration" 2> /dev/null || true
+git -C "$R" checkout -q -- . 2> /dev/null || true
+echo "audit written: .orchestration/validation/$T-audit-$S7.md (+ .last.md)"
+tail -1 "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md"
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
@@ -1,15 +1,25 @@
 #!/usr/bin/env bash
 # orch-gate.sh <task id> <full head sha> <pr>: run the integration gate from the review worktree at the head with the task's evidence copied in.
 set -euo pipefail
-T="$1"; HEAD="$2"; PR="$3"; S7="${HEAD:0:7}"
-MAIN=~/Workspace/dotfiles; R="$MAIN/.claude/worktrees/orchestrator-review"
+T="$1"
+HEAD="$2"
+PR="$3"
+S7="${HEAD:0:7}"
+MAIN=~/Workspace/dotfiles
+R="$MAIN/.claude/worktrees/orchestrator-review"
 cd "$MAIN"
-[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || { echo "review worktree not clean"; exit 2; }
+[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || {
+    echo "review worktree not clean"
+    exit 2
+}
 git -C "$R" checkout -q --detach "$HEAD"
 mkdir -p "$R/.orchestration/validation" "$R/.orchestration/acceptance"
 for f in ".orchestration/validation/$T-pr-feedback.json" ".orchestration/validation/$T-audit-$S7.md" ".orchestration/validation/$T-audit-$S7.md.last.md" ".orchestration/validation/$T-review-receipt.md" ".orchestration/validation/$T-crit.json" ".orchestration/acceptance/$T.md"; do cp "$f" "$R/$f"; done
 set +e
-( cd "$R" && AUDIT_EVIDENCE=".orchestration/validation/$T-audit-$S7.md" AUDIT_DISPOSITIONS=".orchestration/acceptance/$T.md" AGENT_REVIEWED=1 REVIEW_EVIDENCE=".orchestration/validation/$T-review-receipt.md" BASE=origin/main PR_FEEDBACK_EVIDENCE=".orchestration/validation/$T-pr-feedback.json" make require-crit-review ) 2>&1 | tail -15
+(cd "$R" && AUDIT_EVIDENCE=".orchestration/validation/$T-audit-$S7.md" AUDIT_DISPOSITIONS=".orchestration/acceptance/$T.md" AGENT_REVIEWED=1 REVIEW_EVIDENCE=".orchestration/validation/$T-review-receipt.md" BASE=origin/main PR_FEEDBACK_EVIDENCE=".orchestration/validation/$T-pr-feedback.json" make require-crit-review) 2>&1 | tail -15
 rc=${PIPESTATUS[0]}
-git -C "$R" checkout -q -- . 2>/dev/null; git -C "$R" clean -fdq .orchestration; git -C "$R" checkout -q --detach origin/main
-echo "gate rc=$rc"; exit $rc
+git -C "$R" checkout -q -- . 2> /dev/null
+git -C "$R" clean -fdq .orchestration
+git -C "$R" checkout -q --detach origin/main
+echo "gate rc=$rc"
+exit $rc
diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh.orig .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh.orig
+++ .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
@@ -4,10 +4,13 @@
 MAIN=~/Workspace/dotfiles
 S=/private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad
 WT="$S/t717-prep"
-cd "$MAIN"; git fetch -q origin main
+cd "$MAIN"
+git fetch -q origin main
 [ -d "$WT" ] || git worktree add --detach "$WT" origin/main > /dev/null
-cd "$WT"; git checkout -q --detach origin/main; git reset -q --hard
-uv run --no-project python - <<'PY'
+cd "$WT"
+git checkout -q --detach origin/main
+git reset -q --hard
+uv run --no-project python - << 'PY'
 import pathlib
 p = pathlib.Path("home/dot_agents/agent-config.yaml"); s = p.read_text()
 def rep(old, new):
diff home/dot_claude/hooks/executable_project-map-reload.sh.orig home/dot_claude/hooks/executable_project-map-reload.sh
--- home/dot_claude/hooks/executable_project-map-reload.sh.orig
+++ home/dot_claude/hooks/executable_project-map-reload.sh
@@ -31,15 +31,15 @@
 if path == "~" or path.startswith("~/"):
     path = os.path.expanduser("~") + path[1:]
 print(os.path.realpath(path))
-' "$1" 2>/dev/null
+' "$1" 2> /dev/null
 }
 
-file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
+file_path=$(jq -r '.tool_input.file_path // empty' 2> /dev/null) || exit 0
 [[ -n "$file_path" ]] || exit 0
 event_path=$(canonical_path "$file_path") || exit 0
 [[ "$event_path" == */.project-map/index.html ]] || exit 0
 
-listing=$(terminal-browser ls --all --json 2>/dev/null) || exit 0
+listing=$(terminal-browser ls --all --json 2> /dev/null) || exit 0
 candidates=$(jq -c '
     [.browsers[]? | .cdpPort as $port
      | select($port | type == "number")
@@ -48,7 +48,7 @@
      | select(.url | strings | startswith("file://"))
      | select(.targetId | strings | test("^[A-Fa-f0-9]{32}\\z"))
      | [$port, .targetId, .url]][]
-' <<< "$listing" 2>/dev/null) || exit 0
+' <<< "$listing" 2> /dev/null) || exit 0
 selection=""
 while IFS= read -r candidate; do
     [[ -n "$candidate" ]] || continue
@@ -59,12 +59,12 @@
     break
 done <<< "$candidates"
 if [[ -z "$selection" ]]; then
-    terminal-browser open "$file_path" --split right --size 0.5 --no-merge >/dev/null 2>&1
+    terminal-browser open "$file_path" --split right --size 0.5 --no-merge > /dev/null 2>&1
     exit 0
 fi
 IFS=$'\t' read -r port target_id <<< "$selection"
 
 agent="${TERMINAL_BROWSER_AGENT:-$HOME/.local/share/terminal-browser/app/agent-browser/bin/agent-browser}"
-"$agent" --cdp "$port" --session project-map-reload --pin-tab tab "$target_id" >/dev/null 2>&1 || exit 0
-"$agent" --cdp "$port" --session project-map-reload --pin-tab eval "if (location.href === new URL($selected_url).href) location.reload()" >/dev/null 2>&1
+"$agent" --cdp "$port" --session project-map-reload --pin-tab tab "$target_id" > /dev/null 2>&1 || exit 0
+"$agent" --cdp "$port" --session project-map-reload --pin-tab eval "if (location.href === new URL($selected_url).href) location.reload()" > /dev/null 2>&1
 exit 0
diff tests/install/macos/common/brew.bats.orig tests/install/macos/common/brew.bats
--- tests/install/macos/common/brew.bats.orig
+++ tests/install/macos/common/brew.bats
@@ -16,9 +16,9 @@
     function brew() {
         printf '%s\n' "$*" >> "${BATS_TEST_TMPDIR}/brew-calls"
         case "$*" in
-            "untrust --tap") printf 'Untrusted taps:\n  aws/tap\n  azure/bicep\n  hashicorp/tap\n' ;;
-            "list --formula --full-name") printf 'bash\nazure/bicep/bicep\nhashicorp/tap/packer\n' ;;
-            "list --cask --full-name") printf 'hashicorp/tap/vagrant\n' ;;
+        "untrust --tap") printf 'Untrusted taps:\n  aws/tap\n  azure/bicep\n  hashicorp/tap\n' ;;
+        "list --formula --full-name") printf 'bash\nazure/bicep/bicep\nhashicorp/tap/packer\n' ;;
+        "list --cask --full-name") printf 'hashicorp/tap/vagrant\n' ;;
         esac
     }
 
make: *** [format] Error 1
[exit 2]
```
## 12b. Per file, each with its own exit status: the shfmt check on every file make format flags, at HEAD and at 51ba5801; ruff format on this PR's Python files; prettier on this PR's Markdown records
```console
$ for each file: the tool alone; echo exit
shfmt --diff .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff home/dot_claude/hooks/executable_project-map-reload.sh: HEAD exit 1, 51ba5801 exit 1
shfmt --diff tests/install/macos/common/brew.bats: HEAD exit 1, 51ba5801 exit 1
ruff format --check scripts/lint-comparisons.py: exit 0
ruff format --check tests/unit/test_lint_comparisons.py: exit 0
prettier --check .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a02/task.md: exit 0
[exit 0]
```

# Revise 1 (AGMSG-ACCEPTANCE status=revise round=1, 2026-10-19T21:00:22Z; previous head 1950a4de, the chain's update-branch head)

- Every block below ran inside the sandbox from this worktree at the revise's code head `f6fd955e`. Its only later commit is this records commit.
- R2 is the three checks red at `1950a4de` with this head's test file; R3 to R7 are at the code head. §1 to §12b above stay as round 1's evidence at `5b6c5a8a`.

## R1. Revise 1: the branch, origin/main, the merge-base and this round's commits on the update-branch head 1950a4de
```console
$ git rev-parse HEAD origin/main; git merge-base origin/main HEAD; git log --oneline $PREV..HEAD; git show --stat --format= HEAD -- .orchestration | tail -n 2
f6fd955e3d75eb9cf56167c173b6a20568efa518
c9d99a614173ce4e78a17442fd385504fb287bc3
1eac64a832ade83f9e149be6a329f7e8fa20180f
f6fd955e fix(lint): the Bot's three threads: a backslash-newline continues a double-quoted program's closing-quote search, lines join with no separator, shell comments carry quote state across lines and skip heredoc bodies; revise.yaml (T129 normalised-comparison-lint followup a02, revise 1)
9534b4c8 test(lint): a shell comment past a multi-line program's closing quote marks a hit on its earlier line (T129 normalised-comparison-lint followup a02, revise 1)
a4523856 test(lint): the continued jq program's hit is expected at its operator's own line (T129 normalised-comparison-lint followup a02, revise 1)
e8830ee8 test(lint): the three Bot threads of 26f48973: a jq program continued by backslash-newline, a backslash-newline joining a word, a marker inside a multi-line string or heredoc body (T129 normalised-comparison-lint followup a02, revise 1)
 .../revise.yaml                                                    | 7 +++++++
 1 file changed, 7 insertions(+)
[exit 0]
```
## R2. RED at 1950a4de (its lint), with this head's test file, in a scratch worktree: the three checks of the revise
```console
$ git -C "$R" rev-parse --short=8 HEAD; git show HEAD:tests/unit/test_lint_comparisons.py > "$R/tests/unit/test_lint_comparisons.py"; cd "$R" && uv run python -m unittest $CHECKS 2>&1 | /usr/bin/grep -E "^FAIL:|^AssertionError|^Ran|^(OK|FAILED)" | sed -E "s/ \(tests\.unit\.test_lint_comparisons\.LintComparisonsTest\.[a-z0-9_]+\)//" | cut -c1-200
1950a4de
FAIL: test_a_jq_program_continued_by_backslash_newline_is_located_and_r3_applies (fixture='jc.sh')
AssertionError: 1 != 0 : 
FAIL: test_a_jq_program_continued_by_backslash_newline_is_located_and_r3_applies (fixture='jc2.sh')
AssertionError: 1 != 0 : 
FAIL: test_a_backslash_newline_joins_the_physical_lines_without_a_separator (fixture='wj.sh')
AssertionError: Tuples differ: (1, True) != (0, False)
FAIL: test_a_marker_inside_a_multiline_string_or_heredoc_body_is_not_a_comment (fixture='ms.sh')
AssertionError: Tuples differ: (0, '') != (1, 'ms.sh:2: R0 the allow marker carries no reason\n')
FAIL: test_a_marker_inside_a_multiline_string_or_heredoc_body_is_not_a_comment (fixture='ms2.sh')
AssertionError: Tuples differ: (0, '') != (1, 'ms2.sh:2: R0 the allow marker carries no reason\n')
FAIL: test_a_marker_inside_a_multiline_string_or_heredoc_body_is_not_a_comment (fixture='hd.sh')
AssertionError: Tuples differ: (0, '') != (1, 'hd.sh:2: R0 the allow marker carries no reason\n')
FAIL: test_a_marker_inside_a_multiline_string_or_heredoc_body_is_not_a_comment (fixture='hd2.sh')
AssertionError: Tuples differ: (0, '') != (1, 'hd2.sh:2: R0 the allow marker carries no reason\n')
Ran 3 tests in 1.027s
FAILED (failures=7)
[exit 0]
```
## R3. GREEN at the code head: the whole module, verbose
```console
$ git rev-parse --short=8 HEAD; uv run python -m unittest tests/unit/test_lint_comparisons.py -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
f6fd955e
test_a_backslash_newline_joins_the_physical_lines_without_a_separator (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_backslash_newline_joins_the_physical_lines_without_a_separator) ... ok
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_hit_in_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_in_a_changed_file_fails) ... ok
test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... ok
test_a_jq_program_continued_by_backslash_newline_is_located_and_r3_applies (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_jq_program_continued_by_backslash_newline_is_located_and_r3_applies) ... ok
test_a_marker_inside_a_multiline_string_or_heredoc_body_is_not_a_comment (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_marker_inside_a_multiline_string_or_heredoc_body_is_not_a_comment) ... ok
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... ok
test_a_stale_row_for_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_a_changed_file_fails) ... ok
test_a_stale_row_for_an_unchanged_file_warns (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_an_unchanged_file_warns) ... ok
test_each_owned_row_is_refused_or_accepted_by_its_fixture (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_owned_row_is_refused_or_accepted_by_its_fixture) ... ok
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (tests.unit.test_lint_comparisons.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... ok
test_the_changed_files_are_clean_against_the_baseline (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_changed_files_are_clean_against_the_baseline) ... ok
test_the_jq_normaliser_is_required_on_each_operand_side (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails) ... ok
Ran 18 tests in 14.809s
OK
[exit 0]
```
## R4. Every fix is load-bearing: one mutant per fix (the gaps, the worker review round, this revise), each failing its own fixture or check (the script, then its run over the whole module)
```console
$ cat "$TMPDIR/mut-l02.py"; uv run --no-project python -I "$TMPDIR/mut-l02.py" "$Q"
# Each mutant reverts one fix of followup-a02 (the gaps, then the worker review's round); its fixture must fail.
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); f = root / "scripts/lint-comparisons.py"; src = f.read_text()
M = {  # what the mutant reverts -> (the fixed text, the mutant)
    "continuations (4306643800 audit:4f5be51:4)": ('if (len(code) - len(code.rstrip("\\\\"))) % 2:', 'if False:'),
    "shell markers in comments (audit:4f5be51:8 k.sh)": ('        return comments(text)', '        return dict(enumerate(text.split("\\n"), 1))'),
    "python markers in comment tokens (4306643808 m.py)": ('return {t.start[0]: t.string for t in toks if t.type == tokenize.COMMENT}',
                                                        'return dict(enumerate(text.split("\\n"), 1))'),
    "jq strings and comments (audit:4f5be51:5)": ('bare, lits = jq_mask(prog)', 'bare, lits = prog, prog'),
    "and/or bounds (audit:4f5be51:1)": ('(?:and|or|then|elif|else)(?!\\w)"', '(?!)"'),
    "double-quoted programs (4306643803 audit:4f5be51:9)": ("""('[^']*'|"(?:[^"\\\\]|\\\\[\\s\\S])*")""", "('[^']*')"),
    "every escaped fragment (4306643804 audit:4f5be51:2)": ('all(map(escaped, values))', 'all("re.escape" in map(dotted, ast.walk(v)) for v in values)'),
    "the pgrep pattern word expands (audit:4f5be51:6)": ('any(map(expands, PGREP.findall(line)))', 'any("$" in w for w in PGREP.findall(line))'),
    "the grep pattern word expands (audit:4f5be51:3)": ('if ere and expands(pattern)', 'if ere and "$" in pattern'),
    "path pieces beside expansions (audit:4f5be51:7)": ('return bool(name and TOKEN.search(name.group(1))) or bool(',
                                                      'return bool(TOKEN.search(name.group(1))) if name else bool('),
    "review: one slot per string character, the P1 (s2.sh)": ('code[i : i + step], lits[i : i + step] = [" "] * step, prog[i : i + step]',
                                                          'code[i], lits[i : i + len(two)] = " ", (two if c == "\\\\" else c)'),
    "review: if...end is one operand (l2.sh)": ('"( ", re.sub(r"(?<![\\w.$])end(?!\\w)", "  )", bare)', '"; ", re.sub(r"(?<![\\w.$])end(?!\\w)", "  ;", bare)'),
    "review: a marker on any line of a continued statement (c2.sh)": ('for k in range(n, last + 1)', 'for k in range(n, n + 1)'),
    "review: a shell comment past the closing quote (k2.sh)": ('after = comments(code[close:].split("\\n", 1)[0]).get(1, "")', 'after = ""'),
    "review: no program past a separator (j3.sh)": ("""[^'"\\\\\\n;&|])*+""", """[^'"\\\\\\n])*+"""),
    "review: a quote ending its line opens a program (j2.sh)": ('(?=[^\\n]*\\S)', ''),
    "review: a join's separator is a constant (r2.py)": (' and isinstance(node.func.value, ast.Constant)', ''),
    "revise 1: a backslash-newline continues the closing-quote search (jc.sh, jc2.sh)": ('"(?!(?:[^"\\\\\\n]|\\\\[\\s\\S])*")', '"(?!(?:[^"\\\\\\n]|\\\\.)*")'),
    "revise 1: lines join with no separator (wj.sh)": ('buf += code[:-1]  #', 'buf += code[:-1] + " "  #'),
    "revise 1: quotes carried across lines (ms.sh, ms2.sh)": ('        return comments(text)', '        return {n: comments(raw).get(1, "") for n, raw in enumerate(text.split("\\n"), 1)}'),
    "revise 1: heredoc bodies hold no comment (hd.sh, hd2.sh)": ('        if docs and not q:\n            skip = docs.pop(0)', '        if False:\n            skip = docs.pop(0)'),
}
test = "tests.unit.test_lint_comparisons"
for name, (a, b) in M.items():
    assert src.count(a) == 1, (name, src.count(a))
    f.write_text(src.replace(a, b))
    r = subprocess.run(["uv", "run", "python", "-m", "unittest", test], cwd=root, capture_output=True, text=True)
    failed = sorted({(l.split("fixture=")[1].rstrip(")") if "fixture=" in l else l.split()[1]) for l in r.stderr.splitlines() if l.startswith("FAIL")})
    print(f"{name}: {'killed' if r.returncode else 'SURVIVED'}; failing fixtures: {', '.join(failed) or '-'}")
f.write_text(src)
continuations (4306643800 audit:4f5be51:4): killed; failing fixtures: 'c.sh', 'wj.sh', (failures=2)
shell markers in comments (audit:4f5be51:8 k.sh): killed; failing fixtures: 'hd.sh', 'hd2.sh', 'k.sh', 'k3.sh', 'ms.sh', 'ms2.sh', (failures=6)
python markers in comment tokens (4306643808 m.py): killed; failing fixtures: 'm.py', (failures=1)
jq strings and comments (audit:4f5be51:5): killed; failing fixtures: 's.sh', (failures=2), test_a_jq_normaliser_name_inside_a_string_literal_is_no_application
and/or bounds (audit:4f5be51:1): killed; failing fixtures: 'l.sh', (failures=1)
double-quoted programs (4306643803 audit:4f5be51:9): killed; failing fixtures: 'j.sh', 'j2.sh', 'jc.sh', 'jc2.sh', (failures=5), test_a_single_quoted_jq_option_value_is_not_read_as_the_program
every escaped fragment (4306643804 audit:4f5be51:2): killed; failing fixtures: 'r.py', 'r2.py', (failures=2)
the pgrep pattern word expands (audit:4f5be51:6): killed; failing fixtures: 'p2.sh', (failures=1)
the grep pattern word expands (audit:4f5be51:3): killed; failing fixtures: 'g.sh', (failures=1)
path pieces beside expansions (audit:4f5be51:7): killed; failing fixtures: 'v.sh', (failures=1)
review: one slot per string character, the P1 (s2.sh): killed; failing fixtures: 's2.sh', (failures=1)
review: if...end is one operand (l2.sh): killed; failing fixtures: 'l2.sh', (failures=1)
review: a marker on any line of a continued statement (c2.sh): killed; failing fixtures: 'c2.sh', (failures=1)
review: a shell comment past the closing quote (k2.sh): killed; failing fixtures: 'k4.sh', (failures=1)
review: no program past a separator (j3.sh): killed; failing fixtures: 'j3.sh', (failures=1)
review: a quote ending its line opens a program (j2.sh): killed; failing fixtures: 'j2.sh', (failures=1)
review: a join's separator is a constant (r2.py): killed; failing fixtures: 'r2.py', (failures=1)
revise 1: a backslash-newline continues the closing-quote search (jc.sh, jc2.sh): killed; failing fixtures: 'jc.sh', 'jc2.sh', (failures=2)
revise 1: lines join with no separator (wj.sh): killed; failing fixtures: 'wj.sh', (failures=1)
revise 1: quotes carried across lines (ms.sh, ms2.sh): killed; failing fixtures: 'hd.sh', 'hd2.sh', 'ms.sh', 'ms2.sh', (failures=4)
revise 1: heredoc bodies hold no comment (hd.sh, hd2.sh): killed; failing fixtures: 'hd.sh', 'hd2.sh', (failures=2)
[exit 0]
```
## R5. The tracked tree: --all from this head equals --all from 1950a4de's lint (no hit added or removed); the Check's no-flag lint exits 0
```console
$ git show $PREV:scripts/lint-comparisons.py > scripts/.lint-prev.py; uv run --no-project python -I scripts/.lint-prev.py --all > "$TMPDIR/r5-a.txt"; rm -f scripts/.lint-prev.py; uv run --no-project python -I scripts/lint-comparisons.py --all > "$TMPDIR/r5-b.txt"; cmp "$TMPDIR/r5-a.txt" "$TMPDIR/r5-b.txt" && echo "--all identical to 1950a4de's lint"; uv run --no-project python -I scripts/lint-comparisons.py; echo "lint exit $?"
--all identical to 1950a4de's lint
warning: scripts/check-regime-boundary.sh:125: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
warning: scripts/orchestrator/chain-integrate.sh:93: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
warning: scripts/orchestrator/chain-integrate.sh:106: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
warning: scripts/orchestrator/regime-ci.py:65: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
warning: scripts/orchestrator/regime-ci.py:71: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:72: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:90: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:246: R4 Python compares a path or URL by its string form
warning: 8 unbaselined hit(s) and 0 stale row(s) in unchanged files
lint exit 0
[exit 0]
```
## R6. ruff check and ruff format --check on the two files; --list-rules byte-identical to origin/main's
```console
$ ruff check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py; echo "ruff check exit $?"; ruff format --config ruff.toml --check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py; echo "ruff format exit $?"; git show origin/main:scripts/lint-comparisons.py > "$TMPDIR/lm.py"; uv run --no-project python -I "$TMPDIR/lm.py" --list-rules > "$TMPDIR/r-old.txt"; uv run --no-project python -I scripts/lint-comparisons.py --list-rules > "$TMPDIR/r-new.txt"; cmp "$TMPDIR/r-old.txt" "$TMPDIR/r-new.txt" && echo "--list-rules identical"
All checks passed!
ruff check exit 0
2 files already formatted
ruff format exit 0
--list-rules identical
[exit 0]
```
## R7. Caps over origin/main...HEAD (additions plus deletions; the baseline outside the first count)
```console
$ B=$(git merge-base origin/main HEAD); echo "merge-base ${B:0:8}"; git diff --numstat "$B...HEAD" -- . ":!.orchestration"; git diff --numstat "$B...HEAD" | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1 + \$2; next} \$3 == \"scripts/lint-comparisons-baseline.tsv\" {b += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/, without the baseline: %d of 350\nunder tests/: %d of 1000\nthe baseline (outside the count): %d\n\", o, t, b}"
merge-base 1eac64a8
3	1	scripts/lint-comparisons-baseline.tsv
147	32	scripts/lint-comparisons.py
114	0	tests/unit/test_lint_comparisons.py
outside tests/ and .orchestration/, without the baseline: 179 of 350
under tests/: 114 of 1000
the baseline (outside the count): 4
[exit 0]
```
