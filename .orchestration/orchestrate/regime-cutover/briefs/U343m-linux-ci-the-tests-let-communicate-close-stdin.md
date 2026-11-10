# U343m round 10 of U343 (test-only): the four broker tests that close the client's stdin before `communicate()` leave the close to `communicate()`, so they run on the runner's Python 3.12

GOAL
PR 720's head 426188c6 has a correct audit (verdicts/U343l-426188c6.md) and a 0-finding sweep (run-68), but CI's `test (ubuntu-24.04, client)` and `test (ubuntu-24.04, server)` fail: four tests of `tests/unit/test_acp_broker.py` error with `ValueError: flush of closed file` raised inside `client.communicate(timeout=120)` (`:927`, `:966`, `:1100`, `:1181`), each one line after an explicit `client.stdin.close()`. Measured cause: CPython 3.12's `Popen._communicate` flushes `self.stdin` before closing it and raises on a closed file; 3.13 and later tolerate it (a prototype with `Popen(['cat'])`, `stdin.write`, `stdin.close`, `communicate` raises under uv's Python 3.12.15 and returns under 3.13.16 and 3.15.2). The runner's python is `/usr/lib/python3.12`; this host's default is 3.15, which is why the six-module runs of rounds 4 to 9 were green here. The branch's Linux unit tests last ran at fd94feae (round 3); the pull_request workflows did not run on rounds 4 to 9 (the pull request conflicted with main), so the four sites, written in U343g and U343h, met Python 3.12 for the first time at this head. The other 24 broker tests pass on the runner. This round removes the explicit close at the four sites: `communicate()` with no input flushes and closes stdin itself on every CPython, so the client sees the same end of stream.

SCOPE
The worker repository `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U343j` on branch `fix/acp-broker-round8` at 426188c6ed4b7edcaaa33d2cee9f9b94618f15a2 (one new commit on top). May write: `tests/unit/test_acp_broker.py` at the four sites alone. Non-goals: every lever, every copy, the manifest (no lever changes, so no pin changes), the README, the PR body (the coordinator keeps it), any other test.

CONTEXT
The four sites, each `client.stdin.close()` then `out, err = client.communicate(timeout=120)`: `:926-927` (test (c) of U343g, the worker tail without a newline), `:965-966` (test (d) of U343g, the trailer-shaped line then handler loss; the close follows `os.kill(pid, signal.SIGKILL)`), `:1099-1100` (test (a) of U343h, the link planted at the temporary name), `:1180-1181` (test (c) of U343h, the tampered helper). `client_popen` opens the client with `stdin=PIPE, stdout=PIPE, stderr=PIPE`. CPython's `_communicate` (POSIX): when `self.stdin` is set and `input` is None it flushes stdin, then closes it, then reads stdout and stderr to EOF; so deleting the explicit close line changes nothing the client observes (the end of its stdin comes at the same point, after the test's last write and flush) and the ValueError cannot arise. Grep `stdin.close()` in the module: exactly these four lines; every other test already lets `communicate()` close.

DATA SHAPE
No data shape changes. The four tests' observable assertions (the client's exit status, stdout and stderr bytes, the record's content) are unchanged.

CHANGE
1. Reproduce: `uv run --python 3.12 --with pyyaml python -m unittest tests.unit.test_acp_broker.AcpBrokerTest.test_c_a_worker_tail_without_a_newline_is_payload_and_the_client_learns_the_ref_from_the_record -v` at 426188c6 errors with the ValueError (the lines kept in `/tmp/u343m/red.txt`). 2. Delete the four `client.stdin.close()` lines (`:926`, `:965`, `:1099`, `:1180`); touch nothing else. 3. `uv run --python 3.12 --with pyyaml python -m unittest tests.unit.test_acp_broker -v` OK (the 28 tests, the Linux-only and root-only skips as on this host), and `uv run --with pyyaml python -m unittest tests.unit.test_acp_broker -v` (the default interpreter) OK; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `make render-check` exit 0 (nothing generated changes). 4. Commit unsigned: `test(acp-broker): the four tests that closed the client's stdin before communicate() leave the close to communicate(), which Python 3.12 requires (regime-cutover U343m, round 10; CI test (ubuntu-24.04) at 426188c6)` ending with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

ACCEPTANCE
1. The red run of CHANGE 1 at 426188c6 (the `ValueError: flush of closed file` line) pasted; the same test OK at the head under Python 3.12, pasted. 2. `uv run --python 3.12 --with pyyaml python -m unittest tests.unit.test_acp_broker -v` OK at the head, the `Ran N tests` and `OK (skipped=...)` lines pasted. 3. The default-interpreter run of the module OK, lines pasted. 4. `git diff --stat 426188c6 HEAD` shows one file, 4 deletions, 0 insertions, pasted; `grep -c 'stdin.close()' tests/unit/test_acp_broker.py` prints 0. 5. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0 and `make render-check` exit 0, pasted.

VERIFY
ACCEPTANCE pasted into the report; the coordinator fetches the head by path, pushes it onto `feat/acp-broker-lever`, and CI, the sweep and the audit under `--cyber-program daybreak_blue` run at it; then `pr-merge.sh`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts CPython's documented `communicate()` (flush and close of stdin when no input is given) as the one close the client needs, the Python 3.12 run through uv as the runner's interpreter, and the module's own assertions as the proof that the clients' observable behaviour is unchanged; it changes no lever and reads no store.

TIMEBOX
30 minutes.

FORBIDDEN
No change outside the four lines; no rebase; no `git stash`; no push; no `gh` call; no network beyond uv's fetch of Python 3.12 (already cached on this host at `uv python list`); no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u343m/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/.local/state/regime-store/dotfiles/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the program store; you stop at the committed head in `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U343j`. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U343m-progress.txt` after each CHANGE step; final report to `/tmp/dotfiles-wt/U343m-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`.

REPORT
Status, the head (40 hex), the ACCEPTANCE lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 44, 46, 49); decisions row 2026-11-10T11:2xZ (the measured cause); `verdicts/U343l-426188c6.md`.
