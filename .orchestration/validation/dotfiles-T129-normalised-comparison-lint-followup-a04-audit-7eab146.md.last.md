Audited [PR #432](https://github.com/mryfmo/dotfiles/pull/432) at `7eab146d`. The task digest matches dispatch; caps pass at 408/450 changed production lines and 346/1200 added test lines. All 22 selected fixture tests passed in memory. The final-tree scan confirms 97 hits and no stale baseline rows.

[P1] high orchestration .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md:304 The sandbox violation remains applicable: task lines 144 and 206 explicitly supersede older command exceptions, while sandbox.md:18 records unsandboxed `agmsg-dispatch`; citing the older Playbook exception does not resolve that contradiction.

[P2] high implementation scripts/lint-comparisons.py:176 Wrapper options lose their operands: `exec -a label jq 'select(.path == $p)'` produces no R3 because `label` becomes the presumed command; `exec -a label [ "$path" = /x ]` similarly loses R1.

[P2] high implementation scripts/lint-comparisons.py:305 `env LC_ALL=C jq 'select(.path == $p)'` produces no R3, whereas the merge-base implementation detects it; restricting recognition to the first command word without handling `env` introduces a regression.

[P2] high implementation scripts/lint-comparisons.py:184 Selecting one boundary command from a pipeline stage misses producers elsewhere in that stage: both `{ ps aux; :; } | grep service` and `(ps aux && :) | grep service` evade R5; the latter was detected at the merge base.

[P2] high implementation scripts/lint-comparisons.py:280 The recursive test search includes comparisons inside command substitutions, then reports them again as outer comparisons; `[[ $(\n if [[ $path == /x ]]; then echo y; fi\n) == y ]]` emits R1 on both lines 1 and 2 although only line 2 compares a path.

[P2] high implementation scripts/lint-comparisons.py:318 jq markers enter a shared physical-line map and suppress other statements: `jq 'select(.path == $p)'; jq '. # lint-comparisons: allow second-only'` produces no R3 for the first program.

[P2] high implementation scripts/lint-comparisons.py:317 `setdefault` discards a jq comment when a shell comment occupies the same source line: `jq '. # lint-comparisons: allow' # ordinary comment` produces no R0, defeating the newly added reasonless-marker check.

[P2] high implementation scripts/lint-comparisons.py:349 A normaliser mentioned inside an unused function body counts as applied: `def canonical_path: ascii_downcase; (def unused: canonical_path; .path) == ($p | canonical_path)` passes lint although the left operand remains raw; actual jq execution confirms this distinction.

[P2] high implementation scripts/lint-comparisons.py:396 Fully escaped concatenations regress: `re.search(f"{re.escape(prefix) + re.escape(name)}", text)` emits R6, while the merge-base implementation accepts it. Assignment to a05 records ownership but does not fix the defect.

[P2] high orchestration .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md:304 The recorded revise action lacks the required a04 counter output and pasted repeated-class search. Only predecessor a02 counters appear, despite further `hand-parser` findings requiring S1/S2 assessment before dispatch.

[P2] high orchestration .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md:325 The re-plan claims shell facts never come from raw-line searches, but `accepted()` still searches raw source at scripts/lint-comparisons.py:271; `[[ $path == /realpath ]]` is incorrectly accepted merely because the literal contains a normaliser name.

[P2] high evidence .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/report.md:169 The latest correction is called “round 1 of 2,” although lines 89–94 already record the pre-push correction in `d74204e6`; under task line 214, `863f88e3` consumes the second round.

[P3] high evidence .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/validation.md:583 The original 34-mutant evidence filters stderr and retains only four matching lines, contrary to the required complete outputs; the later nine-mutant log does not restore those missing records.

Not checked: full-suite/Bats reruns or live CI; `gh` and the web fallback failed. Saved feedback reports successful final-head checks. Nothing was modified.

INV-6: violated .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md:304 — required counter/search evidence is absent, and correction accounting understates the two rounds already consumed.
Orchestration findings: 3
Verdict: incorrect