#!/usr/bin/env python3
"""Run Bats with a per-test time bound that fails a stalled test by name (regime-cutover U99).

`run-bats.py <bats arguments>` runs `bats --formatter cat <arguments>`, Bats' extended stream, whose
`begin <n> <name>` line names each test as it starts, and prints the TAP lines of that stream with Bats'
exit status. When a test has no result within BATS_PER_TEST_TIMEOUT seconds (default 900), or the stream
is silent that long outside a test (loading a file), it prints `not ok <n> <name> # timeout after <s> s`,
kills Bats and every process it started, and exits 124.

Bats starts in a session of its own, so it inherits neither the caller's process group nor its terminal.
A descendant can leave its process group (job control, `setpgid`) but not the session, and one that
calls setsid() is still found by parent pid: the stop freezes every process of the session and of Bats'
process tree with SIGSTOP until the set stops growing (a stopped process cannot fork, and a stopped
parent keeps its children's parent pid), then sends SIGKILL to all of them and waits until none is left.
A process owned by another user (`sudo …`) is signalled through `sudo -n kill` when the plain signal is
refused. The same sweep runs after a normal end, so no process Bats started outlives the run.

Only `monitor` is dropped from an exported SHELLOPTS: job control is not wanted in Bats' shells, while
bashcov's exported xtrace (and its BASH_XTRACEFD, which is why no descriptor is closed) must reach them.
A run whose plan is `1..0`, or that prints no plan, fails: every suite CI runs has at least one test.
"""

from __future__ import annotations

import os
import selectors
import shutil
import signal
import subprocess
import sys
import time

# Ten times the slowest passing test measured on main (`[ubuntu-client] misc`, 89 s on ubuntu-24.04,
# October 2026) and four times the slowest test of a passing run on a slow mirror (`ghostty`, 214 s).
DEFAULT_BOUND = 900


def child_env() -> dict[str, str]:
    env = dict(os.environ)
    if "SHELLOPTS" in env:
        options = [option for option in env["SHELLOPTS"].split(":") if option and option != "monitor"]
        if options:
            env["SHELLOPTS"] = ":".join(options)
        else:
            del env["SHELLOPTS"]
    return env


def process_table() -> dict[int, int]:
    """Every live process's parent pid, from `ps -A -o pid= -o ppid= -o stat=` (the same on Linux and macOS).

    A zombie has exited and holds no descriptor, so it is left out; its parent or init reaps it.
    """
    out = subprocess.run(
        ["ps", "-A", "-o", "pid=", "-o", "ppid=", "-o", "stat="], capture_output=True, text=True, check=False
    )
    table = {}
    for line in out.stdout.splitlines():
        fields = line.split()
        if len(fields) == 3 and fields[0].isdigit() and fields[1].isdigit() and not fields[2].startswith("Z"):
            table[int(fields[0])] = int(fields[1])
    return table


def members(bats: subprocess.Popen[bytes]) -> set[int]:
    """The live processes of Bats' session and their process trees, Bats included while it runs.

    Once Bats is reaped its pid may belong to an unrelated process, so only the session counts then.
    """
    table = process_table()
    leader = bats.pid
    me = os.getpid()
    found = {pid for pid in table if pid != me and session_of(pid) == leader}  # lint-comparisons: allow integer-pids
    if bats.poll() is None and leader in table:
        found.add(leader)
    children: dict[int, list[int]] = {}
    for pid, parent in table.items():
        children.setdefault(parent, []).append(pid)
    queue = list(found)
    while queue:
        for child in children.get(queue.pop(), []):
            if child not in found:
                found.add(child)
                queue.append(child)
    return found


def session_of(pid: int) -> int | None:
    try:
        return os.getsid(pid)
    except OSError:
        return None


def send(pid: int, sig: signal.Signals) -> None:
    try:
        os.kill(pid, sig)
    except ProcessLookupError:
        pass
    except PermissionError:
        # A process another user owns, such as the root command under `sudo`.
        if shutil.which("sudo"):
            subprocess.run(
                ["sudo", "-n", "kill", f"-{sig.name.removeprefix('SIG')}", str(pid)],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
            )  # fmt: skip


def stop_all(bats: subprocess.Popen[bytes]) -> list[int]:
    """Freeze and kill Bats and everything it started; return the pids that outlived the kill."""
    stopped: set[int] = set()
    for _ in range(100):
        fresh = members(bats) - stopped
        if not fresh:
            break
        for pid in fresh:
            send(pid, signal.SIGSTOP)
        stopped |= fresh
    for pid in stopped:
        send(pid, signal.SIGKILL)
    deadline = time.monotonic() + 10
    while True:
        bats.poll()
        table = process_table()
        survivors = sorted((stopped & table.keys()) | members(bats))
        if not survivors or time.monotonic() > deadline:
            return survivors
        for pid in survivors:
            send(pid, signal.SIGKILL)
        time.sleep(0.05)


def report_survivors(survivors: list[int]) -> None:
    if survivors:
        print(f"run-bats: processes outlived SIGKILL: {' '.join(map(str, survivors))}", file=sys.stderr)


def main(argv: list[str]) -> int:
    bound = int(os.environ.get("BATS_PER_TEST_TIMEOUT", DEFAULT_BOUND))
    bats = subprocess.Popen(
        ["bats", "--formatter", "cat", *argv],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, env=child_env(), start_new_session=True, close_fds=False,
    )  # fmt: skip
    assert bats.stdout is not None
    stream = bats.stdout.fileno()
    selector = selectors.DefaultSelector()
    selector.register(stream, selectors.EVENT_READ)
    running, plan, timed_out, pending = "", None, False, b""
    deadline = time.monotonic() + bound
    # Once Bats has exited, a process it left behind may hold the stream open; reading stops 2 s later.
    exited_at = None
    out = sys.stdout

    def emit(raw: bytes) -> None:
        nonlocal running, plan, deadline
        line = raw.decode(errors="replace")
        if line.startswith("begin "):
            running = line[len("begin ") :]
            deadline = time.monotonic() + bound
            return
        if line.startswith("suite "):
            return
        if line.startswith(("ok ", "not ok ")):
            running = ""
        elif plan is None and line.startswith("1.."):
            plan = line[len("1..") :]
        # A test's own output lines do not extend its bound.
        if not running:
            deadline = time.monotonic() + bound
        out.write(line + "\n")

    while True:
        now = time.monotonic()
        if now >= deadline:
            timed_out = True
            break
        if exited_at is None and bats.poll() is not None:
            exited_at = now
        if exited_at is not None and now - exited_at >= 2:
            break
        if not selector.select(min(deadline - now, 0.5)):
            continue
        chunk = os.read(stream, 65536)
        if not chunk:
            break
        pending += chunk
        *lines, pending = pending.split(b"\n")
        for raw in lines:
            emit(raw)
        out.flush()
    if pending:
        emit(pending)
    if timed_out:
        if running:
            out.write(f"not ok {running} # timeout after {bound} s (BATS_PER_TEST_TIMEOUT); stopping Bats\n")
        else:
            out.write(
                f"not ok - Bats printed nothing for {bound} s outside a test (BATS_PER_TEST_TIMEOUT); stopping Bats\n"
            )
        out.flush()
        report_survivors(stop_all(bats))
        return 124
    out.flush()
    try:
        status = bats.wait(timeout=max(deadline - time.monotonic(), 1))
    except subprocess.TimeoutExpired:
        out.write(f"not ok - Bats closed its output but did not exit within {bound} s (BATS_PER_TEST_TIMEOUT)\n")
        out.flush()
        report_survivors(stop_all(bats))
        return 124
    # Nothing Bats started outlives the run, a process a test left in the background included.
    left_behind = members(bats)
    if left_behind:
        print(f"run-bats: Bats exited and left {len(left_behind)} process(es) running; stopping them", file=sys.stderr)
    report_survivors(stop_all(bats))
    if status == 0 and (plan is None or not plan.isdigit() or int(plan) == 0):
        shown = plan if plan is not None else "nothing"
        print(f"run-bats: expected at least one test; Bats planned {shown}", file=sys.stderr)
        return 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
