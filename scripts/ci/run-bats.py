#!/usr/bin/env python3
"""Run Bats and name the test that outlives its time bound (regime-cutover U99).

`run-bats.py <bats arguments>` runs `bats --formatter cat <arguments>`, Bats' extended stream, and prints its TAP
lines. Each `begin <n> <name>` line becomes `running: <n> <name>`, so a log that stops shows the test it stopped in.
When a test has no result within BATS_PER_TEST_TIMEOUT seconds (default 1200), or the stream is silent that long
outside a test (Bats sources every file before its plan line), it prints `not ok <n> <name> # timeout after <s> s`
and exits 124.

It signals nothing. Stopping a stalled test is the workflow step's `timeout-minutes` and the runner's job: when the
step's main process exits while orphans still hold its output, the runner ends the step after 5 s (actions/runner
ProcessInvoker.ProcessExitedHandler), and it ends the job's orphan processes when the job completes.

A run whose plan is `1..0`, or that prints no plan, fails: every suite CI runs has at least one test.
"""

import os
import selectors
import subprocess
import sys
import time

# 1.5 times the slowest passing test measured on main (`[ubuntu-client] ghostty`, 796 s on ubuntu-26.04 in run
# 40225977873, October 2026); a typical run's slowest test is `[ubuntu-client] misc` at 66-103 s.
DEFAULT_BOUND = 1200
# Once Bats has exited, a process it left behind may still hold the stream open; reading stops this much later.
AFTER_EXIT = 2


def main(argv):
    bound = int(os.environ.get("BATS_PER_TEST_TIMEOUT", DEFAULT_BOUND))
    bats = subprocess.Popen(["bats", "--formatter", "cat", *argv], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE)
    stream = bats.stdout.fileno()
    selector = selectors.DefaultSelector()
    selector.register(stream, selectors.EVENT_READ)
    state = {"running": "", "plan": None, "deadline": time.monotonic() + bound}
    out = sys.stdout

    def emit(raw):
        line = raw.decode(errors="replace")
        if line.startswith("begin "):
            state["running"] = line[len("begin ") :]
            state["deadline"] = time.monotonic() + bound
            out.write(f"running: {state['running']}\n")
            return
        if line.startswith("suite "):
            return
        if line.startswith(("ok ", "not ok ")):
            state["running"] = ""
        elif state["plan"] is None and line.startswith("1.."):
            state["plan"] = line[len("1..") :]
        # A test's own output lines do not extend its bound.
        if not state["running"]:
            state["deadline"] = time.monotonic() + bound
        out.write(line + "\n")

    pending, exited_at = b"", None
    while True:
        now = time.monotonic()
        if now >= state["deadline"]:
            if state["running"]:
                out.write(f"not ok {state['running']} # timeout after {bound} s (BATS_PER_TEST_TIMEOUT)\n")
            else:
                out.write(f"not ok - Bats printed nothing for {bound} s outside a test (BATS_PER_TEST_TIMEOUT)\n")
            out.flush()
            return 124
        if exited_at is None and bats.poll() is not None:
            exited_at = now
        if exited_at is not None and now - exited_at >= AFTER_EXIT:
            break
        if not selector.select(min(state["deadline"] - now, 0.5)):
            continue
        chunk = os.read(stream, 65536)
        if not chunk:
            break
        *lines, pending = (pending + chunk).split(b"\n")
        for raw in lines:
            emit(raw)
        out.flush()
    if pending:
        emit(pending)
    out.flush()
    try:
        status = bats.wait(timeout=max(state["deadline"] - time.monotonic(), 1))
    except subprocess.TimeoutExpired:
        out.write(f"not ok - Bats closed its output but did not exit within {bound} s (BATS_PER_TEST_TIMEOUT)\n")
        out.flush()
        return 124
    plan = state["plan"]
    if status == 0 and (plan is None or not plan.isdigit() or int(plan) == 0):
        print(f"run-bats: expected at least one test; Bats planned {plan or 'nothing'}", file=sys.stderr)
        return 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
