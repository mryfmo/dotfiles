#!/usr/bin/env python3
"""Run Bats and name the test that outlives its time bound (regime-cutover U99).

`run-bats.py <bats arguments>` runs `bats --formatter cat <arguments>`, Bats' extended stream, and prints its TAP
lines. Each `begin <n> <name>` line becomes `running: <n> <name>`, so a log that stops shows the test it stopped in.
When a test has no result within BATS_PER_TEST_TIMEOUT seconds (default: DEFAULT_BOUND below), or the stream is silent that long
outside a test (Bats sources every file before its plan line), it prints `not ok <n> <name> # timeout after <s> s`,
then a read-only diagnosis as TAP comments: every process under Bats as a tree, with its elapsed time, state, Linux
wchan and full command (or `diagnosis unavailable: <reason>` when `ps` fails or hangs), and exits 124.

With `--timing` among the arguments (run_bats in scripts/run_unit_test.sh passes it), every result line carries
` in <ms>ms` after the test's name (RESULT below, the form recorded from Bats 1.14.0 in
tests/fixtures/run-bats/timing-stream.txt); the run's largest duration is printed after the stream's last line as
`slowest: <n> <name> <ms> ms`. A result line without the suffix is a malformed stream: one stderr line names it, and
the exit status stays the suite's. When GITHUB_STEP_SUMMARY names a file, the stall's `not ok` line and diagnosis, or
the slowest line of a passing run, are appended to it in a fenced block under the Bats command (regime-cutover U128).

It signals nothing. Stopping a stalled test is the workflow step's `timeout-minutes` and the runner's job: when the
step's main process exits while orphans still hold its output, the runner ends the step after 5 s (actions/runner
ProcessInvoker.ProcessExitedHandler), and it ends the job's orphan processes when the job completes.

A run whose plan is `1..0`, or that prints no plan, fails: every suite CI runs has at least one test.
"""

import os
import re
import selectors
import shlex
import subprocess
import sys
import time

# Passing Ubuntu client runs spend 66-103 s on their slowest test (`[ubuntu-client] misc`); the 796-1077 s outliers
# (ghostty, misc) fetched from a slow azure.archive.ubuntu.com node (actions/runner-images#14823), which CI now drops
# (scripts/ci/drop-azure-apt-mirror.py). Twice the bound (one earlier test as slow as it allows, then the stalled
# one) plus what the other tests take (at most 284 s measured) stays under the `Run unit test` step's timeout-minutes,
# so a stalled test is named and diagnosed before the step is stopped (tests/unit/test_apt_mirror.py BoundOrderTest).
# The `slowest:` line every run prints under `--timing` (and writes to the job summary page) is what these figures
# are re-checked against (U128); a bound here is never moved on a guess.
DEFAULT_BOUND = 600
# Once Bats has exited, a process it left behind may still hold the stream open; reading stops this much later.
AFTER_EXIT = 2
# The diagnosis' one `ps` call gets this long; a hung `ps` leaves the timeout's exit unchanged.
PS_TIMEOUT = 10
# A result line under `--timing`, as Bats 1.14.0 prints it (tests/fixtures/run-bats/timing-stream.txt): the duration
# follows the name, before any ` # skip <reason>` directive. The name is read lazily, so a reason that holds
# ` in <n>ms` is not read as the duration.
RESULT = re.compile(r"(?:ok|not ok) (?P<number>\d+) (?P<name>.+?) in (?P<ms>\d+)ms( # .*)?")


def trace_fds():
    """The descriptor bashcov traces through (BASH_XTRACEFD), to pass to Bats; Popen closes every other one.

    Unset or empty: none. 0-2 need no passing. Anything else must name an open descriptor, or the run fails here
    instead of losing the coverage trace silently.
    """
    value = os.environ.get("BASH_XTRACEFD", "")
    if not value:
        return ()
    if not value.isdigit():
        sys.exit(f"run-bats: BASH_XTRACEFD={value!r} is not a descriptor number")
    fd = int(value)
    try:
        os.fstat(fd)
    except OSError as error:
        sys.exit(f"run-bats: BASH_XTRACEFD={fd} is not an open descriptor ({error.strerror})")
    return () if fd <= 2 else (fd,)


def wchan(pid):
    """The kernel function a Linux process sleeps in (/proc/<pid>/wchan), or `-` where there is none to read."""
    try:
        with open(f"/proc/{pid}/wchan") as handle:
            return handle.read().strip() or "-"
    except OSError:
        return "-"


def diagnosis(root):
    """TAP comment lines showing every process under Bats (pid root), as a tree: pid, elapsed time, state, wchan and
    the full command, so a timed-out test's log names the command it stalled in. Read-only: one bounded `ps` call,
    whose failure is reported instead of the tree."""
    try:
        listed = subprocess.run(
            ["ps", "-e", "-o", "pid=", "-o", "ppid=", "-o", "etime=", "-o", "stat=", "-o", "args="],
            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=PS_TIMEOUT, check=False,
        )  # fmt: skip
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"# diagnosis unavailable: {error}\n"
    if listed.returncode != 0:
        return f"# diagnosis unavailable: ps exited {listed.returncode}: {listed.stderr.strip()}\n"
    rows, children = {}, {}
    for line in listed.stdout.splitlines():
        fields = line.split(None, 4)
        if len(fields) < 4 or not fields[0].isdigit() or not fields[1].isdigit():
            continue
        pid, parent = int(fields[0]), int(fields[1])
        rows[pid] = (fields[2], fields[3], fields[4] if len(fields) > 4 else "")
        children.setdefault(parent, []).append(pid)
    if root not in rows:  # lint-comparisons: allow integer-pids
        return f"# diagnosis unavailable: Bats (pid {root}) is not in ps's list\n"
    text = ["# diagnosis: the processes under Bats (pid, elapsed, state, wchan, command)\n"]
    stack = [(root, 0)]
    while stack:
        pid, depth = stack.pop()
        elapsed, stat, args = rows[pid]
        text.append(f"#   {'  ' * depth}{pid} {elapsed} {stat} {wchan(pid)} {args}\n")
        stack.extend((child, depth + 1) for child in sorted(children.get(pid, ()), reverse=True))
    return "".join(text)


def summary(text):
    """Append text to the file GITHUB_STEP_SUMMARY names (the run's summary page), in a fenced block so GitHub shows
    the lines as written. Unset or empty: nothing. A write that fails is one stderr line; the exit status is the
    caller's either way (the summary is a convenience, the log is the record)."""
    path = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if not path:
        return
    try:
        with open(path, "a") as handle:
            handle.write(f"```text\n{text}```\n")
    except OSError as error:
        print(f"run-bats: GITHUB_STEP_SUMMARY={path!r} not written: {error.strerror}", file=sys.stderr)


def main(argv):
    bound = int(os.environ.get("BATS_PER_TEST_TIMEOUT", DEFAULT_BOUND))
    timing = any(argument in ("--timing", "-T") for argument in argv)
    command = ["bats", "--formatter", "cat", *argv]
    bats = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, pass_fds=trace_fds())
    stream = bats.stdout.fileno()
    selector = selectors.DefaultSelector()
    selector.register(stream, selectors.EVENT_READ)
    state = {"running": "", "plan": None, "slowest": None, "deadline": time.monotonic() + bound}
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
            if timing:
                result = RESULT.fullmatch(line)
                if result is None:
                    print(
                        f"run-bats: malformed stream: no duration on a result line under --timing: {line}",
                        file=sys.stderr,
                    )
                elif state["slowest"] is None or int(result["ms"]) > state["slowest"][0]:
                    state["slowest"] = (int(result["ms"]), result["number"], result["name"])
        elif state["plan"] is None and line.startswith("1.."):
            state["plan"] = line[len("1..") :]
        # A test's own output lines do not extend its bound.
        if not state["running"]:
            state["deadline"] = time.monotonic() + bound
        out.write(line + "\n")

    def stalled(verdict):
        """The stall's `not ok` line and the diagnosis, to stdout and to the summary; the exit is 124."""
        text = f"{verdict}\n{diagnosis(bats.pid)}"
        out.write(text)
        out.flush()
        summary(f"{shlex.join(command)}\n{text}")
        return 124

    pending, exited_at = b"", None
    while True:
        now = time.monotonic()
        if now >= state["deadline"]:
            if state["running"]:
                return stalled(f"not ok {state['running']} # timeout after {bound} s (BATS_PER_TEST_TIMEOUT)")
            return stalled(f"not ok - Bats printed nothing for {bound} s outside a test (BATS_PER_TEST_TIMEOUT)")
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
        return stalled(f"not ok - Bats closed its output but did not exit within {bound} s (BATS_PER_TEST_TIMEOUT)")
    plan = state["plan"]
    if status == 0 and (plan is None or not plan.isdigit() or int(plan) == 0):
        print(f"run-bats: expected at least one test; Bats planned {plan or 'nothing'}", file=sys.stderr)
        status = 1
    if state["slowest"] is not None:
        ms, number, name = state["slowest"]
        line = f"slowest: {number} {name} {ms} ms\n"
        out.write(line)
        out.flush()
        if status == 0:
            summary(f"{shlex.join(command)}\n{line}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
