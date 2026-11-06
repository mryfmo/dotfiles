# U241b the late-holder test lands its holder by handshake, not by a 50 ms sleep

GOAL
`tests/unit/test_trusted_exec_contract.py::test_the_holder_scan_waits_for_a_reader_whose_open_has_not_returned` (lines 614 to 650 at main) failed the macOS test leg of PR 695 on 2026-11-06 with the scan answering `by no process whose descriptors this user can read (0 unreadable)` instead of naming pid 4242: the test builds the holder in a thread after `time.sleep(0.05)` and renames it into the fake proc tree, expecting the scan to be mid-walk at that moment; on a loaded runner the scan finished before the holder appeared. U241 (PR 678) removed the same premise from the sibling test by a handshake on the scan's own per-pid listing. This unit applies the same form here: the scan cannot pass its first pass of the (empty) proc tree until the holder is in place, and the holder's own open-not-returned condition stays what the test is about.

SCOPE
A new branch `fix/late-holder-test-handshake` from `origin/main` (your tree is `/tmp/dotfiles-wt/U241b`). May write: `tests/unit/test_trusted_exec_contract.py` (that one test and a helper it alone uses) and the body `../U241b-pr-body.md`. Not: the module under test (`tests/unit/trusted_exec_contract.py`), any other test.

CONTEXT
Read the test whole and U241's test (`test_the_holder_scan_opens_no_fifo`, lines 565 to 640 at main) for the handshake form: a wrapped `os.listdir` (`tec.os.listdir`) that sets an `inside` event on its first call and waits on a second event. Here the scan walks an empty `proc` first (the holder is renamed in later), so the hook sits on the scan's listing of the proc root: the first listing of `proc` sets `inside`, then waits for `placed`, which the late-holder thread sets right after its `os.rename`; the scan then lists `proc` and finds pid 4242. The 50 ms sleep goes. The second half of the test (the `never` probe with an empty proc and `waited < 2`) stays as it is.

DATA SHAPE
Two events and one hook, as in U241: `inside` set by the scan's first `os.listdir(proc)`, `placed` set by the holder thread after `os.rename`; the hook waits on `placed` (30 s) before calling through, only for the proc root and only on its first call. The holder thread waits on `inside` before building, so the holder is renamed in while the scan is provably mid-walk, not after a timer.

CHANGE
1. The handshake per DATA SHAPE; the comment rewritten in the U234 and U241 style (what the test proves, why the holder is handshaken, the PR 695 run).
2. Mutation check, not committed: make the scan skip a holder whose `fd` listing is empty (or otherwise break the wait-for-reader behaviour the test protects), run the test, confirm it fails, revert with `git checkout -- <path>`, paste both.
3. The body `../U241b-pr-body.md`: Summary, Contract (guarantee: the test fails when the scan stops waiting for a reader whose open has not returned, and passes regardless of scheduler order), Verification (ACCEPTANCE pasted), the mutation check.

ACCEPTANCE
1. 20 runs of the single test print `OK` twenty times; 5 runs under a two-core `yes` load print `OK` five times (paste the counts).
2. `uv run python -m unittest tests.unit.test_trusted_exec_contract tests.unit.test_scratch_git` OK (paste the count).
3. The mutation check pasted.
4. `grep -c 'time.sleep(0.05)' tests/unit/test_trusted_exec_contract.py` prints 0 (or names the other sleeps that remain and why).
5. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. CI's macOS leg on the PR is the coordinator's evidence.

CLOSURE
remove

TRUST
TRUST: the unit trusts the holder scan's listing of the fake proc root as the place to hook and U241's handshake as the form; it changes no production code and reads no network.

TIMEBOX
30 minutes.

FORBIDDEN
No change to the module under test that survives the mutation check; no sleep, bound or retry added; no change to any other test; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u241b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 58)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U241b` and the coordinator fetches it by path.
- Progress line beside your tree (`../U241b-progress.txt`) every ten minutes at most; first edit within ten minutes. Write your final report to `../U241b-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes; Test Behavior, Not Implementation).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the hook you chose with its `file:line`, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 44, 46); `AGENTS.md` (Test Policy); PR 678 (U241) as the sibling fix.
