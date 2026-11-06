# U234b the two linear-time tests judge against a baseline measured alongside, not against a fixed bound

GOAL
U234 (PR 676) widened the judged step of the two linear-time tests in `tests/unit/test_validate_agent_assets.py` to 8,000 to 64,000 with bound 24 and interleaved repetitions. On the macOS test leg the class returned twice this morning on healthy code: PR 686 at 09:2xZ and PR 680 at 09:5xZ, both `test_a_generic_rule_scans_a_padded_line_in_linear_time` over the bound (`after / before` at the 8x step), each costing an empty commit and a CI cycle while every other leg was green. A fixed ratio bound on a shared, loaded macOS runner is the premise that keeps failing (order 33: a treadmill changes approach). This unit removes the premise: the test measures a known-linear reference scan over the same inputs in the same process, interleaved with the scan under test, and judges the scan under test against that reference (the ratio of ratios), so a load burst that hits both alike cancels and only a super-linear scan fails.

SCOPE
A new branch `test/linear-time-tests-judge-against-a-baseline` from `origin/main` (your tree is `/tmp/dotfiles-wt/U234b`). May write: `tests/unit/test_validate_agent_assets.py` (the two tests `test_a_generic_rule_scans_a_padded_line_in_linear_time` and `test_the_report_of_many_findings_in_one_file_is_linear_in_the_findings`, and one shared helper they alone use), and the body `../U234b-pr-body.md`. Not: `scripts/validate-agent-assets.py` (the scanner under test is unchanged), any other test.

CONTEXT
Read the two tests whole (around lines 2780 to 2900 at main) and U234's docstring (the history of the bounds and the runs). The scanner's work per character is the thing under test; a reference that is linear by construction over the same input sizes is `len(re.findall(r".", text))` or a `for ch in text: pass` loop, or `text.count(" ")`, run with the same five interleaved repetitions and the same least-of-five rule. The judged quantity becomes `(scan_after / scan_before) / (ref_after / ref_before)`, which is about 1 for a linear scan and about 8 for a quadratic one at the 8x step; the bound 3 keeps a comfortable margin on both sides. Keep the sizes, the two padding kinds and the three forms U234 named.

DATA SHAPE
One helper `linear_growth(scan, sizes, repetitions=5)` that returns, for the step, the least-of-five time of the scan at each size and the least-of-five time of the reference at each size, measured interleaved (size A scan, size A reference, size B scan, size B reference, five times), and the ratio of ratios. The two tests assert the ratio of ratios is under 3 and print the four times and both ratios in the failure message.

CHANGE
1. The helper and the two tests per DATA SHAPE; the docstrings record this round (the two macOS failures of 2026-11-06 with their PR numbers) in U234's style.
2. Run each test 20 times locally and 5 times under a two-core `yes` load as U241 did; paste the counts.
3. The body `../U234b-pr-body.md`: Summary (the premise and its removal), Contract (guarantee: the tests fail for a scan whose growth at the 8x step is three times a linear reference's and pass for a linear one whatever the runner's load, as long as the load hits the interleaved pair alike; leaves out: the scanner), Verification (ACCEPTANCE pasted), and a mutation check: a quadratic stand-in (U234's body named one) fails the new judgment.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_scratch_git` OK (paste the count).
2. 20 runs of each test: `OK` twenty times each; 5 runs under load: `OK` five times each (paste the counts).
3. The mutation check pasted (the quadratic stand-in fails with the ratio named).
4. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. CI's macOS leg on the PR is the coordinator's evidence.

CLOSURE
remove

TRUST
TRUST: the unit trusts the in-process reference scan as linear by construction and the interleaved measurement as sharing the runner's load; it changes no production code and reads no network.

TIMEBOX
40 minutes.

FORBIDDEN
No change to the scanner; no new bound widening; no skip on macOS; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u234b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 58)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U234b` and the coordinator fetches it by path.
- Progress line beside your tree (`../U234b-progress.txt`) every ten minutes at most; first edit within ten minutes. Write your final report to `../U234b-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Attack the Premise; Explain the Number).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 35, 37, 41, 44, 46); `AGENTS.md` (Test Policy); PR 676 (U234) and PR 678 (U241) as the sibling fixes.
