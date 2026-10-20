[P2] high implementation scripts/lint-comparisons.py:75 `pgrep -f "$1"` now produces no R5, whereas the base flags it. Expansion detection accepts only letter-prefixed variables, dropping positional and special parameters.

[P2] high implementation scripts/lint-comparisons.py:129 Double-quoted jq continuations become newlines instead of disappearing. Splitting `==` or `.path` across a backslash-newline therefore bypasses R3, although Bash supplies the intact operator or identifier to jq.

[P2] high implementation scripts/lint-comparisons.py:125 Only the first quoted fragment of a jq argument is scanned. `jq -r 'select(''.url == $p)'` produces no R3, although the shell passes `select(.url == $p)` as one argument.

[P2] high implementation scripts/lint-comparisons.py:98 Arithmetic shifts such as `bits=$((1 << shift))` enter heredoc state. Subsequent comments disappear from classification, suppressing reasonless-marker R0 findings and rejecting legitimately marked comparisons.

[P2] high implementation scripts/lint-comparisons.py:180 Heredoc bodies remain in shell-rule scanning after their comments are excluded. A quoted heredoc containing `[[ $path == /x ]] # lint-comparisons: allow reason` now generates R1 for literal data; the base accepts it.

[P2] high implementation scripts/lint-comparisons.py:88 ANSI-C strings mishandle escaped single quotes. After `msg=$'it\'s fine'`, quote state remains open and a valid allow comment on the following comparison is ignored.

[P2] high implementation scripts/lint-comparisons.py:98 Valid heredoc delimiters such as `'123'` and `'END-DATA'` are not recognized. A reasonless marker inside either body incorrectly generates R0, leaving the owned heredoc-comment fix incomplete.

[P2] high specification .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a02.md:72 Amendment 1 replaces the earlier cap but omits its `.orchestration/` exclusion. Its literal count is 1,976 changed lines, exceeding 350; validation reports 179 by applying an exclusion absent from the amended requirement.

[P2] high orchestration .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a02.md:121 “Round 1 of 2” omits the worker’s pre-push review fix in `5b6c5a8a`. Together with `f6fd955e`, this is two fix rounds under the inherited Completion clause, which explicitly counts rounds before the first RESULT.

[P2] high orchestration .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a02.md:142 The advisory dispositions name followup-a03, but the cited hash identifies the already-completed PR #415 predecessor. That task excludes other comparison-rule repairs and assigns its advisory work to a02; its existence does not establish ownership of these new findings.

Seven parser checks, including all 22 owned fixtures, passed in memory. The pinned tree reproduces the reported eight warnings with no stale baseline rows; the task-copy hash matches.

📝 まとめ: 読み取り専用の監査を完了しました。実装上の指摘7件と、仕様・オーケストレーション上の指摘3件が残っています。

The task declares no numbered invariant map; its inherited cap and round requirements assess as follows:

INV-2: violated .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a02.md:72  
INV-6: violated .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a02.md:121

Orchestration findings: 3

Not checked: the full subprocess suite or live CI; `gh` could not connect. Saved CI reports ten successful checks, but the reproduced parser defects remain.
Verdict: incorrect