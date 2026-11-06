# U241 the FIFO scan test lands its poll by handshake, not by scheduler luck

GOAL
`tests/unit/test_trusted_exec_contract.py::test_the_holder_scan_opens_no_fifo` (lines 565 to 612 at d1ecd495) failed the macOS test leg of PR 674 on 2026-11-06 with `AssertionError: 0 not greater than 0 : no poll landed inside the scan`, and the same assertion failed another macOS leg at 00:37Z the same day (the U174 class: a test whose pass depends on the runner's scheduler). The test starts the scan in a thread and polls `opened()` while the thread is alive; on a loaded runner the scan of 501 fake pids finished before the main thread ran once, so no poll landed and the test's own guard fired. The decoys exist only to make the scan last long enough, which is a timing premise. This unit replaces the premise with a handshake: the scan cannot pass its first pid until one poll has landed inside it, so the guard holds by construction and the decoys lose their reason to exist.

SCOPE
A new branch `fix/holder-scan-poll-handshake` from `origin/main` d1ecd495 (your tree is `/tmp/dotfiles-wt/U241`; if it is absent, wait 30 s and look again). May write: `tests/unit/test_trusted_exec_contract.py`, that one test and any helper it alone uses, and the body file `../U241-pr-body.md` beside your tree. Not: `scripts/lib/trusted_exec_contract.py` or whatever module `tec` names (the code under test does not change), any other test.

CONTEXT
Measured at d1ecd495. The test builds a fake `PROC_ROOT` with 500 decoy pids whose `fd/3` links to a planted FIFO and one holder pid 4242; `opened()` reports whether the scan opened the sentinel or the FIFO (a non-blocking write-open answers `ENXIO` only while nobody reads the FIFO); the main thread loops `while scan.is_alive(): assertEqual("", opened()); polls += 1`, then asserts `polls > 0`. U234 (PR 676, d1ecd495) fixed the sibling class in `test_validate_agent_assets.py` by changing what is judged, not by widening a bound; its docstring cites the runs. Read `probe._holders` and the probe class in this test module (`worker_root_probe`, `_open_writer`) to choose the hook: it must sit on a read the scan performs per pid (a directory listing or a link read on the fake proc tree) so the scan is provably mid-walk when it blocks, and it must not touch the opens the test exists to catch.

DATA SHAPE
Two events and one hook. `inside = threading.Event()` is set by the hook on the scan thread before it blocks; `polled = threading.Event()` is set by the main thread after its first `opened()` call returns `""`. The hook wraps the per-pid read the scan already makes (chosen from the probe code, cited in the test comment), sets `inside` on its first call, then waits on `polled` with a timeout of 30 s, then calls through. The main thread waits on `inside` (30 s), polls once, sets `polled`, and keeps polling while the thread is alive as today. The guard becomes `assertTrue(inside.is_set())` plus the existing `assertGreater(polls, 0)`, both now guaranteed by the handshake rather than by the decoys.

CHANGE
1. Add the handshake per DATA SHAPE inside `test_the_holder_scan_opens_no_fifo`. Keep the planted FIFO, the holder pid 4242 and the expected record string unchanged. Cut the decoy count to a handful (the breadth they prove, a second match naming the pid once, is already the `fd/5` link) or remove them if the handshake alone covers what the comment says they were for; say which in the comment.
2. Rewrite the test's leading comment: what the test proves (the scan reads the descriptor table without opening what it finds), why the poll is handshaken (this unit, the two failing macOS legs of 2026-11-06, the 500-decoy timing premise), in the U234 docstring style, no phase narration.
3. Mutation check, not committed: make the scan open the planted FIFO for reading once (a temporary edit in the module under test in your tree), run the test, confirm it fails with `the scan opened the planted FIFO for reading`, revert the edit with `git checkout -- <path>`, and paste both the failure line and the clean `git status` of that path into the body.
4. The body `../U241-pr-body.md`: Summary (the failure, the premise, the handshake), Contract (guarantee: the test fails when the holder scan opens the FIFO or the sentinel, and passes regardless of scheduler order; leaves out: the scan's own behaviour, which is unchanged), Verification (ACCEPTANCE pasted), the mutation check.

ACCEPTANCE
1. `for i in $(seq 1 20); do uv run python -m unittest tests.unit.test_trusted_exec_contract.TrustedExecContractTest.test_the_holder_scan_opens_no_fifo 2>&1 | tail -1; done` prints `OK` twenty times (adjust the class name to the file's; paste the twenty lines or a count of them).
2. The same single test under load: run it 5 times while `yes > /dev/null & yes > /dev/null &` occupy two cores, then kill the `yes` processes; paste the five result lines.
3. `uv run python -m unittest tests.unit.test_trusted_exec_contract tests.unit.test_scratch_git` OK (paste the count).
4. The mutation check of CHANGE 3 pasted.
5. `grep -c 'range(5000, 5500)' tests/unit/test_trusted_exec_contract.py` prints 0.
6. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section. CI's macOS leg on the PR is the coordinator's evidence.

CLOSURE
remove

TRUST
TRUST: the unit trusts the holder scan's current reads of the fake proc tree as the place to hook; it changes no production code and reads no network.

TIMEBOX
40 minutes.

FORBIDDEN
No change to the module under test that survives the mutation check; no bound, sleep or retry added to the test; no change to any other test; no local bats; no network; no push; no `gh` call.

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 50)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U241` and the coordinator fetches it by path.
- Progress line beside your tree (`../U241-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (principles Fix Root Causes and Test Behavior, Not Implementation apply).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the hook you chose with its `file:line`, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37); `AGENTS.md` (Comment Policy, Test Policy); PR 676 (U234) as the sibling fix.
