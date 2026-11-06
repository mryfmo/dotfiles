# U234c the linear-time tests judge CPU time, the minimum of interleaved repeats, against a reference of their own magnitude

GOAL
`tests/unit/test_validate_agent_assets.py::test_a_generic_rule_scans_a_padded_line_in_linear_time` (and its sibling `..._many_findings_...`, the `LinearGrowth` helper at lines 147 to 190 at main) failed the macOS test leg of PR 696 on 2026-11-06 (run 42215027918) with `scan 0.0450 s at 8,000 characters to 0.8383 s at 64,000 (18.6x); reference 0.8153 s to 4.7060 s (5.8x); 3.23x the reference's growth`, bound 3. This is the third failure of this test's lineage on a loaded macOS runner: U234 judged a fixed bound, U234b (PR 695) judged against a linear reference measured alongside, and both share one premise: one wall-clock sample per size judges growth on a runner that runs six unittest shards at once. The numbers show why the premise fails: the reference takes 18x longer than the scan at the small size, so a scheduler slice inflates the scan's 45 ms by a factor it cannot inflate the reference's 815 ms by, and the ratio of ratios swings. This unit replaces the premise: CPU time of this process (`time.process_time_ns`), the minimum of k interleaved repeats per size for both the scan and the reference, and a reference sized to the scan's own magnitude at the small size.

SCOPE
A new branch `test/linear-time-cpu-min-of-repeats` from `origin/main` (your tree is `/tmp/dotfiles-wt/U234c`). May write: `tests/unit/test_validate_agent_assets.py` (the `LinearGrowth` helper, the two tests, the reference work) and the body `../U234c-pr-body.md`. Not: `scripts/validate-agent-assets.py` (the scanner under test), any other test.

CONTEXT
Read the helper and the two tests whole, the U234b body (PR 695, `git log` of the file) and the three failures: U234's at `decisions.tsv` 2026-11-05 (fixed bound), U234b's measurement in its body (20/20 idle, 5/5 under a two-core load), and the row of 2026-11-06T12:2xZ in `decisions.tsv` quoting the numbers above. The premise to write down in the docstring and then abandon: that wall-clock time of one run per size is comparable between a 45 ms workload and an 815 ms one on a shared runner. What a CI runner does to the measurement: six shards in parallel, so the process is descheduled for slices of tens of milliseconds at any point; wall-clock sees every slice, `process_time` sees none of them (it counts only this process's CPU), and the minimum of k repeats discards the runs that were hit by cache or frequency effects.

DATA SHAPE
`LinearGrowth` gains the measurement rule as data: `clock = time.process_time_ns`, `repeats = 5`, and `measure(sizes)` interleaves the scan and the reference at each size (scan small, reference small, scan large, reference large, k times) and keeps the minimum per (workload, size); `judged` is the scan's min-growth divided by the reference's min-growth as now; the bound stays 3. The reference is sized once at import or at test start so that its minimum at the small size is within a factor of 2 of the scan's (a loop count chosen by a short calibration against the scan's small-size minimum, the chosen count asserted in the failure message), so both workloads sit at the same time scale. The quadratic stand-in test (U234b's mutation) stays the proof that the judge separates.

CHANGE
1. The helper per DATA SHAPE; the docstring of each test rewritten in the U234b style: what it proves, the three failures with their numbers, the premise abandoned and the rule that replaces it.
2. Stress measurement on this host, pasted: 20 runs of the two tests idle; 10 runs under CPU oversubscription of twice the core count (`yes > /dev/null &` x 2·ncpu, killed after); 10 runs with the tests' own process pinned alongside a parallel unittest run of two other heavy modules (`test_hcom_seat`, `test_pr_audit`) to mimic the CI shard layout; all OK, or the first failure's numbers and your diagnosis.
3. Mutation check, not committed: the quadratic stand-in (U234b's form) fails the judge with its growth printed; a scan whose padded-line behaviour is made quadratic (if U234b's body shows how) fails; revert, paste.
4. The body: Summary (the three failures, the premise, the rule), Contract (the test fails a quadratic scan and passes a linear one on any scheduler load that leaves the process some CPU; the one residual, CPU-frequency scaling between repeats, is bounded by the minimum of k), Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_validate_agent_assets` OK (paste the count and the wall time; the two tests must finish within 60 s together).
2. The CHANGE 2 counts pasted (20/20, 10/10, 10/10) with the judged values' range.
3. The CHANGE 3 mutation results pasted.
4. `grep -c 'perf_counter' tests/unit/test_validate_agent_assets.py` prints 0 for the two tests' helper (or names the remaining uses and why).
5. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. CI's macOS leg on the PR, three times (the coordinator re-runs it twice with `gh run rerun`), is the coordinator's evidence.

CLOSURE
remove

TRUST
TRUST: the unit trusts `time.process_time_ns` as the CPU clock of this process and the quadratic stand-in as the separation proof; it changes no production code and reads no network.

TIMEBOX
45 minutes.

FORBIDDEN
No change to the scanner; no skip or retry decorator; no widening of the bound above 3; no change to any other test; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u234c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U234c` and the coordinator fetches it by path.
- Progress line beside your tree (`../U234c-progress.txt`) every ten minutes at most; first edit within ten minutes. Write your final report to `../U234c-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Attack the Premise; Explain the Number: every measured ratio in the body says what limited it).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the measurement rule in one line, the stress counts and the judged range, the mutation results, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 44, 46); `AGENTS.md` (Test Policy); PR 695 (U234b) as the previous form; `decisions.tsv` 2026-11-06T12:2xZ (the numbers).
