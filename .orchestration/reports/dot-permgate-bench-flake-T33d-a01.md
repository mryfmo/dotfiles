# T33d report — dot-permgate-bench-flake-T33d-a01 (revision 1)

- worker: `claude-standard-dot-a005`; orchestrator: `claude-remediation-dot`
- worktree: `~/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `test/permgate-bench-flake` from `origin/main` = `7d47e46`
- task_rev: sha256 `30f444a16d404da68e5483c635bc21be2f350cf12138cc498d746634bfaee95c`, checked
- PR: https://github.com/mryfmo/dotfiles/pull/200, head `e161082e393c8fb8622133140da3fda1c9e6b309`
- status: ready_for_review. CI is green on head e161082 after one rerun: the first run's `public-bootstrap (macos-14, client)` failed on a transient Homebrew download HTTP 503, unrelated to this test-only change. All checks pass except nix, which was skipped. Verbatim output is in the validation file.

## Step 1: reproduce and capture the benchmark JSON

I used a scratchpad driver (`permgate_bench_repro.py`) that runs the test's
own `setUp` and then the same `permgate bench` subprocess, and prints each
agent's `n` / `successful_classifications` / `status_counts` /
`latency_ms`. I ran it 3 times with 20 `yes > /dev/null` loops occupying
all 20 cores. Every run failed the same way:

```
{"claude": {"n": 5, "successful_classifications": 5, "status_counts": {"classified": 5}, "latency_ms": [16, 17, 17, 17, 17], ...}}
{"codex":  {"n": 5, "successful_classifications": 0, "status_counts": {"timeout": 5},    "latency_ms": [204, 201, 202, 206, 202], ...}}
```

- The failing agent is always **codex**; claude always succeeds.
- The status is `timeout` for all 5 calls.
- The latency is about 202 ms, which is the fixture policy's
  `timeout_seconds: 0.2`.

## Step 2: diagnosis. The suspected mechanism is refuted; the real one is proven.

- **Suspected: interpreter startup under load. Refuted.** Both fakes are
  Python interpreters started via a shebang, yet under the same load claude
  classified in about 17 ms. With stdin at EOF, codex is also fast under
  full load (about 18 ms).
- **Actual mechanism: codex prompt in argv, stdin left inherited, and a
  fake that reads stdin.**
  - `executable_permgate` `classify()` calls claude with `input=prompt`,
    so the child's stdin reaches EOF.
  - It calls codex with the prompt as the **last argv element** and **no
    stdin argument**, so the child inherits permgate's stdin, which is the
    test runner's stdin.
  - The fixture's default fake codex runs `prompt = sys.stdin.read()`,
    which blocks while that stdin is an open pipe or socket. It is
    released only by the 0.2 s `subprocess` timeout.
- **Evidence (verbatim in the validation file):**
  - Timing the fake codex directly: with inherited stdin (the harness
    socket) it timed out after 5 s in 5/5 calls, both with and without
    load. With `stdin=DEVNULL` it took about 17–25 ms, with and without
    load.
  - `sleep 20 | permgate_bench_repro.py`, an open pipe with **no load**,
    gives codex `{"timeout": 5}` deterministically.
  - `< /dev/null` gives 5/5 classified, both without load and **under full
    load**.
  - `sleep 20 | python3 -m unittest tests.unit.test_permgate -k bench`
    before the fix gives `AssertionError: 0 != 5` (FAILED), deterministic
    and with no load.
- **Why it looked like a load flake:** whether the runner's stdin is an
  open, empty pipe or socket depends on how the suite is launched. In my
  earlier sessions the first full run after an edit hit it and the rerun
  did not.
- **Product defect? Not proven, so product code is untouched.** The fixture
  violated the real contract, because permgate passes the codex prompt in
  argv. Whether the real `codex exec` reads an inherited stdin when a
  positional prompt is given was not verified: that would need a codex
  invocation, which is forbidden. Hardening candidate for a separate,
  product-scoped task: add `stdin=subprocess.DEVNULL` to the codex
  `subprocess.run` in `classify()`, and perhaps in bench too, so the
  classifier never depends on the caller's stdin.

## Step 3: fix (test fixture only, `tests/unit/test_permgate.py`)

1. **Root cause.** The default fake codex now uses `prompt = args[-1]`
   instead of `sys.stdin.read()`, with a comment explaining the contract.
   The capture file keeps `{"args", "prompt"}`, so the no-leak test (which
   asserts the capture contains neither the marker nor `tool_input`) still
   checks the same content.
2. **Headroom**, as the task suggested.
   `test_bench_runs_five_layer_two_fixtures` now calls
   `self.write_policy(timeout=8)`, the maximum the validator allows
   (`0 < timeout_seconds <= 8`). On its own this would **not** have fixed
   the bug: a blocking read on an open pipe would simply wait up to 8 s and
   still time out. The root fix is (1); this is defence in depth against
   genuine CI stalls.
3. **Failure detail.** Every bench assertion now carries
   `"<agent>: <full result JSON>"`, including `status_counts` and
   `latency_ms`, as its message.

## Step 4: proof

- `sleep 20 | python3 -m unittest tests.unit.test_permgate -k bench` after
  the fix: `Ran 2 tests … OK`.
- The same with 20 cores busy: `OK`.
- `sleep 20 | permgate_bench_repro.py` after the fix, using setUp's
  **original 0.2 s policy**, so the headroom does not mask it: codex gets
  5/5 `classified` in about 12 ms. That shows the root cause is fixed, not
  just given more time.
- The full `make unit-test` passes **twice in a row** (494 OK each time),
  plus a third run with an open-pipe stdin (`sleep 120 | make unit-test`),
  also OK. `make validate-agent-assets` passes.

## CompactionDB

The mechanism wording is adjusted to what step 2 proved, as the task
instructs:

[memory:decision] T33d: the permgate bench unit test flaked because the fixture fake codex
read stdin while permgate passes the codex prompt as argv and leaves stdin inherited, so
the fake blocked on the test runner open stdin until the 0.2s policy timeout (not CPU
load: /dev/null stdin passes under full load, an open pipe fails without load); fixed in
the test fixture (fake codex takes the prompt from its last argument, max
validator-allowed 8s headroom for the bench, full per-agent result in the failure
message), product code untouched (operator 2026-09-28).

Id `ee4256a6-39e0-4788-af4c-2b5a31055d02`; the output is in the validation
file.

## Effects

None outside the repository. The CPU-load generator was 20 short-lived
`yes > /dev/null` processes, killed right after each measurement. The only
other writes outside the worktree were the `.orchestration` artifacts and
the local CompactionDB ledger.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
