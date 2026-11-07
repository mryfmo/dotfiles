# U318c round 3 of U318: seat-login-preflight normalises the root's spelling before the link test, refuses a failed predicate, and the launcher-side test exists

GOAL
The round-2 audit of PR 716 (`verdicts/U318b-ad9b9456.md`, correct, merged as 668ba887) filed two code findings under the weight threshold in `scripts/orchestrator/seat-login-preflight`, and its body named one launcher-side test as owned by this unit. (1) Line 320 at ad9b9456: a `REGIME_SEATS_ROOT` spelled with a trailing `//` (`<link>//`) makes `-L` follow the link, so `--check` exits 0 and profile mode creates `.state/claude` through the link, against the component-validation guarantee of round 2. (2) Line 327: a failed file predicate is read as absence, so an owned root with mode 000 hides a linked `.state`; `--check` reports `absent` with exit 0 and profile mode fails at `mkdir` with exit 1 instead of the component refusal. (3) `tests/unit/test_hcom_seat.py` has no test that the launcher propagates the preflight's component refusal (exit 2 and its text) to the seat launch; the round-2 body's orchestrator-effect row is out-of-scope with this unit as owner.

SCOPE
A new branch `fix/seat-login-preflight-root-spelling-and-predicates` from `origin/main` 668ba887; the tree is `/tmp/dotfiles-wt/U318c`. May write: `scripts/orchestrator/seat-login-preflight` and its byte-identical copy `home/dot_local/bin/common/executable_seat-login-preflight`, `tests/unit/test_remote_host_logins.py` (`PreflightTest`), `tests/unit/test_hcom_seat.py` (one new test), the regenerated `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (by `uv run --with pyyaml python scripts/generate-agent-configs.py` only), and the body `../U318c-pr-body.md`. Not: `hcom-seat`, any doc.

CONTEXT
Read `verdicts/U318b-ad9b9456.md` whole (its Reproduced section describes the two scratch probes: the `//` spelling and the mode-000 root). Read the lever whole: the shared three-component validation of round 2 (`claude_config_validate`), where the seats root comes from (`REGIME_SEATS_ROOT` or the checkout-derived root), the `-L`, `-d`, `-O` tests on each component, and how `hcom-seat` runs the preflight and propagates its status (`hcom-seat:2359` at 668ba887, `|| exit $?`). The round-2 tests (`PreflightTest`, 25 tests) run the lever from the checkout under a scratch HOME with a fake `claude`; `test_hcom_seat.py` has the launcher fixture (`held_launch`, the fake tools on PATH) that round-1 and round-2 of U318 used for the shim tests.

DATA SHAPE
The seats root is one normalised spelling before any test: trailing slashes removed (a bare `/` stays `/`), no `.` or `..` components, judged by `[[ ${root} == */ ]]` loops or `${root%/}` applied until stable, never by `realpath` (which would follow the link the test must catch). Each component's predicates are three outcomes, not two: holds, does not hold, or could not be evaluated (the parent unsearchable or unreadable, `test` itself failing); the third refuses naming the component and the reason (`cannot read <component> (permission denied)`), never reads as absence. In `hcom-seat`, the preflight's exit status and text pass through unchanged to the launch's refusal; the new test asserts that observable: a planted link at `.state` under the fixture's seats root makes `hcom-seat worker --dry-run` exit 2 with the preflight's component line in stderr and nothing made.

CHANGE
1. Normalise the root spelling once where it enters (both the variable and the derived form) and test every component on the normalised spelling. 2. Make the predicate evaluation three-valued: probe the parent's searchability and the entry's readability (`[[ -x parent ]]`, a `stat`-free `[[ -e ]]` under a checked parent) and refuse by name when the probe cannot run; a mode-000 root with a linked `.state` refuses naming `.state` or the root, never `absent`. 3. Tests in `PreflightTest`: `REGIME_SEATS_ROOT=<link>//` and `<link>/./` refuse naming the component in `--check` and profile mode, nothing created through the link; a mode-000 owned root with a linked `.state` refuses by name in both modes (skip when running as root); the normalisation keeps a plain root's behaviour (the round-2 tests pass unchanged). 4. `tests/unit/test_hcom_seat.py`: `test_a_preflight_component_refusal_stops_the_launch_with_exit_2` (a link at `.state` under the fixture's seats root; the dry run exits 2, stderr holds the preflight's component line, no slot or directory made). 5. `cmp`; the generator; `make render-check`; `uv run --with pyyaml python scripts/validate-agent-assets.py`; `make shellcheck`; `shfmt -i 4 -sr -d` on the lever; `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`. 6. Commit `fix(seat-login): the preflight normalises the root's spelling before the link test and refuses a predicate it cannot evaluate (regime-cutover U318c)` with the trailer. 7. The body: `## Summary`, `## Contract` (TRUST line), `## Threat table` (`row | risk | status | evidence`, one row per changed path, the two pin files in rows of their own, every closed row naming a selector), `## Verification` with every ACCEPTANCE line pasted; `Program-Unit: regime-cutover/U318` once (the parent unit, standing order 24) and the `Generated with [Claude Code]` footer.

ACCEPTANCE
1. `uv run --with pyyaml python -m unittest tests.unit.test_remote_host_logins tests.unit.test_hcom_seat -v` OK (count pasted; the new tests named). 2. The three new preflight tests fail against the 668ba887 lever (a scratch copy of `git show 668ba887:scripts/orchestrator/seat-login-preflight` in place of the lever, the round-2 form) and pass against the head (outputs pasted). 3. `cmp` 0; `make render-check` 0; validate-agent-assets 0. 4. shellcheck 0; shfmt 0; ruff 0; lint-comparisons 0. 5. On a scratch HOME under `/tmp/u318c/`: `REGIME_SEATS_ROOT="$link//" seat-login-preflight --check` exits 2 naming the component and `ls` of the link's target shows nothing created; a mode-000 root with a linked `.state` exits 2 naming it (pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report.

CLOSURE
remove

TRUST
TRUST: the unit trusts the U318 design and the round-2 validation as the model; it changes the spelling normalisation, the predicate evaluation and one launcher test; it reads no credential, logs in nowhere, runs no seat.

TIMEBOX
45 minutes.

FORBIDDEN
No change to `hcom-seat`'s code (one test in its module only); no `realpath` or `pwd -P` on the root before the link test; no doc change; no network; no push; no `gh` call; no pin edited by hand; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u318c/`, then read it); no real `claude auth login`.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U318c`.
- Progress line at `../U318c-progress.txt`; final report to `../U318c-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), `git diff --stat origin/main HEAD`, the ACCEPTANCE lines with their outputs, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46); `verdicts/U318b-ad9b9456.md`; the U318b brief `briefs/U318b-seat-login-preflight-check-validates-the-chain-quotes-the-command-and-reads-the-status-round2.md`.
