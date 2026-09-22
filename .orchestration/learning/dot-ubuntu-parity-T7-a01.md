# dot-ubuntu-parity-T7-a01 — learning triage

## Reusable rule candidates

1. `env PATH=<mock-dir-only> bash <script>` (or `bash -c '...'`) makes `env`
   itself fail to resolve `bash` via that same stripped PATH, exiting 127
   before the script under test ever runs. Any bats test that needs to
   fully control a script's PATH (to simulate a missing tool) must invoke
   the interpreter by absolute path — `/bin/bash` — so `env` execs it
   directly. This repo already had the right convention in
   `tests/install/common/setup.bats`; T4's new tests didn't follow it
   because they were only checked with `bash -n` (syntax only), never
   actually run. Recorded as CompactionDB `[memory:decision]`
   `b3a6c98a-763a-4f64-b803-33c48b3c20dd`.

2. Any bats test that mocks `curl`/`uname`/`sha256sum` together (checksum-
   verified installers) must mock ALL of them consistently, or the pinned
   checksum comparison in the real (unmocked) install-script logic becomes
   host-architecture-dependent and non-deterministic. `zed.bats`'s two
   `zed_artifact`-only tests got this right; the fuller `main` test didn't.

3. A `bash -n` syntax check is not equivalent to actually running a test.
   T4's report claimed "bash -n clean" for the install scripts, which is
   true and necessary, but is a different, weaker check than "the bats
   tests that mock these scripts actually pass" — the latter requires
   `bats -f` on the specific new/changed tests before shipping, restricted
   to tests that don't mutate real system state. This session's standing
   practice going forward: any task that adds a new mock-based bats test
   must run it with `bats -f` before claiming the test suite is healthy,
   even though the _install scripts_ themselves still can't be executed
   for real locally.

## Bug discovered, not fixed (out of this task's scope)

`install/ubuntu/client/zed.sh::install_pinned_zed` moves the extracted app
into `${staging}` before creating `${staging}`'s parent directory
(`${HOME}/.local/share`) — invisible on any real machine, but a real
fresh-bootstrap failure (same class as T5's timer bug). Recorded as
CompactionDB `[memory:failure]` `aac17d27-411a-49f0-a892-b2c47bd3771d` and
flagged in the report as a recommended follow-up task, since
`forbidden_actions` for T7 bars editing install scripts. Worth promoting
to an actual fix task; not promoting to `skills/candidates/` since it's a
one-off script bug, not a reusable workflow.
