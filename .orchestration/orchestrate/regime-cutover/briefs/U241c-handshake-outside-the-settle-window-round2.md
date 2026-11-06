# U241c round 2 of U241b: the handshake must not spend the scan's settle window

GOAL
The round-1 audit of PR 696 (U241b, head 2e364494; `verdicts/U241b-2e364494.md`) found one P1: the hook on the scan's first `os.listdir(proc)` waits for the holder's rename while the scan's settle clock is running (`trusted_exec_contract.py:279-284` at 8f31cf5c: `settle = time.monotonic() + HOLDER_WAIT_S` is taken before the first pass, and a pass that names nobody after `settle` returns without rescanning). The auditor delayed the holder thread's rename by 300 ms and healthy code failed 3/3 with the no-holder record. The test therefore still carries a scheduler premise (the holder thread is woken and renames within 200 ms of `inside`), only a wider one than the 50 ms sleep. This round takes the handshake out of the settle window so the test passes on any scheduler and still fails a scan that stops rescanning.

SCOPE
The existing branch `fix/late-holder-test-handshake` at 2e36449450c22f80ed98346bdf2f855bee1349f6 (your tree is `/tmp/dotfiles-wt/U241c`, already on that head; the PR is 696). May write: `tests/unit/test_trusted_exec_contract.py` (that one test) and the body `../U241c-pr-body.md` (start from `/tmp/dotfiles-wt/U241b-pr-body.md`, add a Round 2 section). Not: the module under test (`tests/unit/trusted_exec_contract.py`), any other test.

CONTEXT
The U241b diff is `git diff origin/main` in your tree; read it and the verdict's Findings and Reproduced sections whole. The scan's settle rule is the behaviour the test protects: a pass naming nobody is repeated every POLL_S until HOLDER_WAIT_S has elapsed. The second probe of the test (the `never` probe with an empty tree, `waited < 2`) already proves the wait is HOLDER_WAIT_S long and no longer, so the first probe does not have to prove the length; it has to prove the rescan happens and finds the holder.

DATA SHAPE
The first probe's own `HOLDER_WAIT_S` set generously (an instance attribute on `probe`, for example 30 s, named in the docstring) so that the time the handshake spends inside the first pass cannot reach `settle`; the handshake itself (two events, the hook on the first listing of the proc root, the holder renamed in and `placed` set) stays as U241b wrote it. With that, the first pass ends on an empty tree with the holder in place, the rescan at POLL_S names pid 4242, and the test finishes in about POLL_S after the rename, regardless of how long the holder thread took to wake. A scan that stops rescanning still returns the no-holder record at once and fails the test. If you find a form that keeps the default HOLDER_WAIT_S and is as simple (for example a patched `tec.time.monotonic` that does not advance while the hook waits), state it in the report with its line count against this one; do not ship both.

CHANGE
1. The change per DATA SHAPE; the docstring's U241b paragraph gains the round-2 sentence (what the auditor injected, why the settle window is now out of the handshake's reach).
2. Two mutation checks, not committed, each reverted with `git checkout -- <path>` and pasted: (a) the auditor's injection, an `os.rename` wrapper (or a sleep before the rename in the holder thread) that delays the rename by 300 ms, run the test 3 times, all OK; then with 2 s, 3 times, all OK; (b) the no-rescan mutation from round 1 (the scan settles after its first pass), the test fails with the no-holder record.
3. The body: the Round 2 section with the finding quoted, the change, the two mutation checks and the ACCEPTANCE lines.

ACCEPTANCE
1. 20 runs of the single test print `OK` twenty times; 5 runs under a two-core `yes` load print `OK` five times (paste the counts).
2. `uv run python -m unittest tests.unit.test_trusted_exec_contract tests.unit.test_scratch_git` OK (paste the count; name any error that is an absent Apple tool on this host, as the auditor saw three).
3. Both mutation checks pasted, with the delay values and the run counts.
4. `grep -c 'time.sleep(0.05)' tests/unit/test_trusted_exec_contract.py` prints 0.
5. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. CI's macOS leg on the PR is the coordinator's evidence.

CLOSURE
remove

TRUST
TRUST: the unit trusts the scan's settle rule as the behaviour under test and U241b's handshake as the form; it changes no production code and reads no network.

TIMEBOX
25 minutes.

FORBIDDEN
No change to the module under test that survives a mutation check; no sleep added to the test's main path; no change to any other test; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u241c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 58)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U241c` and the coordinator fetches it by path.
- Progress line beside your tree (`../U241c-progress.txt`) every ten minutes at most; first edit within ten minutes. Write your final report to `../U241c-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes; Attack the Premise: two fixes shared the premise that the holder thread runs inside the scan's window).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the HOLDER_WAIT_S value or the alternative form, the mutation results, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 44, 46); `AGENTS.md` (Test Policy); `verdicts/U241b-2e364494.md`; PR 678 (U241) as the sibling fix.
