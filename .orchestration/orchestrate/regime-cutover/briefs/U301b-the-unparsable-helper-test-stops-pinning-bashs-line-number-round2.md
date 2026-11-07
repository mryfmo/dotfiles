# U301b round 2 of U301: the unparsable-helper test stops pinning bash's line number

GOAL
CI at the U301 head 182ac480 (PR 709) fails the three Ubuntu test legs in `tests/unit/test_ci_runner.py::InstallerHelperGuardTest::test_a_helper_whose_source_returns_non_zero_refuses_naming_the_installer_and_the_path` (five subtests, one per installer): the `unparsable` subtest asserts `f"{helper}: line 1: syntax error"` (`tests/unit/test_ci_runner.py:378`), the message bash 3.2.57 prints on the macOS host, while bash 5.x on ubuntu-24.04 and 26.04 reports the same error at `line 2` (CI log: `'...ci-runner.sh: line 1: syntax error' not found in '...ci-runner.sh: line 2: syntax er...'`). The macOS leg passed. The test pins an implementation detail of bash's parser message instead of the behavior (the helper's path named, exit 2, nothing on stdout).

SCOPE
The same branch `fix/macos-installers-ci-runner-helper` and PR 709; the tree is `/tmp/dotfiles-wt/U301` at 182ac480. May write: `tests/unit/test_ci_runner.py` (that one assertion and the docstring sentence that promises the message) and the body `../U301b-pr-body.md` (the round-1 body `/tmp/dotfiles-wt/U301-pr-body.final.md` plus a Round 2 paragraph). Not: any installer, any other test.

CONTEXT
Read `InstallerHelperGuardTest` whole (`tests/unit/test_ci_runner.py:304-396`). The `unparsable` subtest exists to show the guard's own branch is never reached for a syntax error; the observable behavior is exit 2, bash's own message naming the helper's path, and an empty stdout. The line number depends on the bash version and is not the kit's behavior.

DATA SHAPE
One assertion on the message's shape independent of the parser's line counter: the stderr holds the helper's path followed by `: line ` and holds `syntax error`; exit 2; stdout empty.

CHANGE
1. `tests/unit/test_ci_runner.py:378`: replace the single `assertIn` with two, `f"{helper}: line "` and `"syntax error"` (or one regular expression `rf"{re.escape(helper)}: line \d+: syntax error"` with `assertRegex`); adjust the docstring sentence so it promises the path and the syntax error, not a line number.
2. Run the module on this host (bash 3.2) and, if `bash` 5.x is on PATH (`mise`, Homebrew), also with `/bin/bash` replaced by that bash in a scratch copy of the test or by setting the test's bash path if it has one; paste both.
3. The body: the round-1 body plus `## Round 2` (the CI failure quoted, the one assertion changed, why the line number is not behavior).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_ci_runner tests.unit.test_scratch_git -v` OK (count pasted).
2. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
3. The bash 5 run of CHANGE 2 pasted, or the line stating no bash 5 is on this host.

VERIFY
ACCEPTANCE pasted into the body's Verification section; CI's Ubuntu legs on the pushed head are the proof.

CLOSURE
remove

TRUST
TRUST: the unit trusts bash's documented behavior that a syntax error in a sourced file is fatal in a non-interactive shell and names the file; it reads no other state, no network, no credential, and runs no package manager.

TIMEBOX
20 minutes.

FORBIDDEN
No change to any installer or to `scripts/lib/ci-runner.sh`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u301b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U301` and the coordinator fetches it by path.
- Progress line at `../U301b-progress.txt` after every step; final report to `../U301b-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Test Behavior, Not Implementation: the path and the error, not the parser's line counter).

REPORT
Status, head sha (40 hex), files changed, the ACCEPTANCE result lines, deviations. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); `verdicts/U301-182ac480.md`; the CI log of run 42310683419 job 128211055700.
