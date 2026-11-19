"""Shared probes of design-quality 5.14 item 7: one attack each in a temporary fixture, and the trusted parent."""

import contextlib
import errno
import functools
import hashlib
import json
import os
import pwd
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

from scratch_git import git_init

SHIMS = ("uv", "python3", "gh", "git", "bash")
ALLOWED = ("PATH", "HOME", "LANG")
SAFE_PATH = "/usr/bin:/bin"
LEGIT, ATTACKER = "legitimate\n", "attacker\n"
BASELINE_NS, NFS = 10**18, "NFSHomeDirectory:"  # a fixed past mtime (2001): a write at any later clock tick moves it
QUIET = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
HOSTILE_GIT_ENV = ("GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CEILING_DIRECTORIES")
HOSTILE_GIT_ENV += ("GIT_ALTERNATE_OBJECT_DIRECTORIES",)
SHIM = "#!{python} -I\nimport json, sys\nwith open({record!r}, 'a') as f:\n    f.write(json.dumps({{'name': {name!r}, 'argv': sys.argv}}) + '\\n')\nsys.exit(97)\n"


class TrustedExecRefused(ValueError):
    """run_under_trusted_parent refused the script before running anything."""


class ShimProbe:
    """Failing shims of SHIMS first on PATH, each recording its name and argv as JSON through an absolute python."""

    def __init__(self, base, env=None):
        if any(c.isspace() for c in sys.executable):
            raise RuntimeError(f"{sys.executable}: a shim interpreter path must hold no whitespace")
        self.base, self.bin, self.record = base, base / "bin", base / "shim-runs.jsonl"
        self.bin.mkdir()
        for name in SHIMS:
            (self.bin / name).write_text(SHIM.format(python=sys.executable, record=str(self.record), name=name))
            (self.bin / name).chmod(0o755)
        self.env = dict(os.environ if env is None else env)
        self.env["PATH"] = os.pathsep.join(filter(None, (str(self.bin), self.env.get("PATH", ""))))

    def records(self):
        return [json.loads(line) for line in (self.record.read_text() if self.record.exists() else "").splitlines()]

    def assert_none_ran(self):
        if runs := self.records():
            raise AssertionError("shim ran: " + "; ".join(f"{r['name']} {r['argv']!r}" for r in runs))


class HostileGit:
    """A legitimate and an attacker repository; attack(kind) yields the environment to offer a consumer."""

    def __init__(self, base):
        self.base, self.legit, self.attacker = base, base / "legit", base / "attacker"
        self.hook_marker, self._env = base / "attacker-hook-ran", {"PATH": SAFE_PATH, "HOME": str(base)}
        for repo, text in ((self.legit, LEGIT), (self.attacker, ATTACKER)):
            repo.mkdir()
            git_init(repo, env=self._env | QUIET)
            (repo / "probe.txt").write_text(text)
            self._git(repo, "add", "probe.txt")  # an index, so status consults core.fsmonitor
        hook = self.attacker / "hook"
        hook.write_text(f'#!/bin/sh\necho ran >> "{self.hook_marker}"\nexit 1\n')
        hook.chmod(0o755)
        self.config = self.attacker / "attacker.gitconfig"  # included, it makes git run the attacker's program
        self.config.write_text(f"[core]\n\tfsmonitor = {hook}\n")

    def _git(self, repo, *args):
        subprocess.run(["/usr/bin/git", "-C", str(repo), *args], env=self._env | QUIET, check=True, capture_output=True)

    @contextlib.contextmanager
    def attack(self, kind):
        """Kind environment exports hostile GIT_*; the local-* kinds plant one key in the fixture's own config."""
        self.hook_marker.unlink(missing_ok=True)
        if kind == "environment":
            git_dir = self.attacker / ".git"
            values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects")
            yield self._env | {name: str(value) for name, value in zip(HOSTILE_GIT_ENV, values, strict=True)}
            return
        pairs = {"local-worktree": ("core.worktree", self.attacker), "local-include": ("include.path", self.config)}
        key, value = pairs[kind]
        self._git(self.legit, "config", key, str(value))
        try:
            yield dict(self._env)
        finally:
            self._git(self.legit, "config", "--unset", key)

    def assert_unaffected(self, root, content):
        """The consumer's confirmed root and what it read there are legitimate, and no attacker program ran."""
        real, found = os.path.realpath(root), []
        if real != str(self.legit):
            found.append(f"attacker root {root}" if real == str(self.attacker) else f"wrong root {root!r}")
        if content != LEGIT:
            found.append("attacker content" if content == ATTACKER else f"wrong content {content!r}")
        found += ["attacker hook ran"] if self.hook_marker.exists() else []
        if found:
            raise AssertionError("hostile git: " + "; ".join(found))


_CONSUMER_ERRORS = {}  # consume()'s worker thread -> its outcome, while it runs
_previous_excepthook = threading.excepthook


def _consumer_excepthook(args):
    """threading.excepthook: a consume() worker's exception goes to its caller, which raises it; any other thread's
    goes to the hook that was installed before (no exception is caught, so none can be swallowed)."""
    outcome = _CONSUMER_ERRORS.get(args.thread)
    if outcome is None:
        _previous_excepthook(args)
    else:
        outcome["error"] = args.exc_value


threading.excepthook = _consumer_excepthook


class WorkerRoot:
    """An input, an output and a new output under a worker root; the consumer runs through consume().

    The input is a FIFO read sentinel, never a regular file: opening it for reading is a kernel event the probe sees
    from outside the consumer. consume(target) runs the consumer step in a worker thread and, while it runs, the
    probe itself alternates a short join with one `os.open(input, O_WRONLY | O_NONBLOCK)`:
      - ENXIO: no process has the input open for reading;
      - success: a reader holds it (the consumer step's thread, a thread it starts, or a subprocess, by any path):
        the read is recorded and the descriptor closed, which gives the reader EOF, so it cannot hang;
      - ENOENT or ELOOP: the input is removed or replaced by a link at this poll, which is recorded;
      - any other errno: recorded as an error, so the check fails closed.
    One last attempt runs after the join. At the deadline the probe makes one more attempt (which releases a reader
    blocked on the sentinel) and waits GRACE_S; a consumer thread still running then fails consume() with
    "consumer thread still running after the deadline". Python cannot stop a thread, so nothing is claimed about it. Between attempts the probe opens and closes a non-blocking reader, so a consumer that opens the input
    for writing is released (its write then fails, EPIPE) instead of waiting for the deadline. No thread runs in the
    probe outside consume(), and stat() opens nothing, so metadata checks never count.

    The input's access time is not used: another process that reads a fresh regular file sets it too (the macOS
    host's Spotlight importer or endpoint scanner reads new temporary files within a second); none of those opened
    a FIFO on macOS, and on 2026-11-04 something on a Linux runner did. The output stays a regular file the consumer
    must not write, checked by inode, mode, mtime and content.

    A recorded read names the processes that hold the sentinel open at the scan, read from /proc on Linux (pid,
    comm, parent pid, command line) before the probe closes its writer, because two 2026-11-04 runs on the
    ubuntu-24.04 server cell saw a reader outside the consumer step and the record could not say which.

    Attribution (U625). A detected open is the consumer's read when the scan names a holder: every process whose
    descriptor table this user can read is this user's (the consumer step's thread, a subprocess it started, or any
    other process of this user), and the lever under test and its descendants run as this user. Nine Unit test jobs
    on GitHub's Ubuntu runners between 2026-10-28 and 2026-11-19 (both flavours, never a macOS leg) failed the
    compliant consumer of test_metadata_reads_and_other_files_are_not_reads_of_the_input with an open of the
    sentinel that named nobody and 146 to 159 unreadable tables (root's: the base directory is 0700, so no place for
    the FIFO keeps such a process out). Rounds 1 (21e0da60) and 2 (e3bff483) of U625 sent an open with no named
    holder to an `unattributed` list on the premise that the /proc scan names every reader of this user. CI at
    21e0da60 refuted the premise (run 44599355380, job 135826206740, the ubuntu-24.04 client leg): in
    test_worker_root_probe [read with os.open] the test's own same-user reader, `os.close(os.open(input,
    O_RDONLY))`, opened the sentinel and closed again before the scan listed it; the scan named nobody with 177
    unreadable tables, the open went to `unattributed`, and the read the test expects went unrecorded. A runner
    always has unreadable tables, so the scan cannot attribute an open that closes at once, and a lever that opens
    and closes the input at once would have been waved through. The rule rests on something else.

    A directory scanner opens what it finds; the lever opens the input it was given. So a control FIFO,
    `.probe-control`, lies beside the input (same directory, same mode, created and removed with the worker root)
    and is watched the same way at every attempt: a non-blocking write-open that does not fail with ENXIO means a
    reader has it open, and the descriptor is closed at once, which gives that reader EOF. An open of the input with
    a named holder is a read, as before. An open with no named holder is a read too, recorded as the pre-U625 string
    with `(control silent)` before it (`<input> (control silent) opened for reading by no process whose descriptors
    this user can read (N unreadable)`), unless the control also had a reader inside the open's window: from
    CONTROL_WINDOW_S before the write-open that detected the open to CONTROL_WINDOW_S after the holder scan ended
    (the writer closes right then, and a scanner that took the input first reaches the control only after that
    close; one that took the control first blocks on the input until the next attempt). Then both opens are a
    scanner's: the record names both, with the unreadable count, the attempts and the UTC time, goes to
    `scanner_opens`, is printed on stderr as `worker root: scanner open: ...` so the job log keeps the case, and
    fails nothing. consume() settles such an open after its last attempt, watching the control until the window has
    closed. The rule is the same on a host without /proc (macOS): nothing names a holder there, so every open is a
    read (`<input> (control silent) opened for reading reader not identified (no /proc)`) unless the control was
    opened too. Left out, what the rule cannot tell: a scanner that opens only files whose names it knows (the input
    alone, never the control) is reported as the lever's read with the control's silence in the record, so the log
    shows the case; a scanner of this user is named by the scan and reported as a read, as before; and on a host
    without /proc a read the lever made while a scanner happened to open the control passes, since no holder can be
    named there (no macOS host has opened a FIFO of the probe so far).

    Scope. The probe detects a blocking read open of the input by the consumer step, and a replacement or removal of
    the input that is present at any poll or at the check. The consumer under test is repository code reviewed in
    the same PR, and the probe guards against an accidental read, not against an adversary inside the test process.
    So it does not claim to detect (residual): a replacement swapped in and restored between two polls (about a
    millisecond apart); reads made by audit hooks or other callbacks running inside the probe's own calls; a read
    open that never blocks (O_NONBLOCK, or O_RDWR) and closes between two polls; a write to the input in place (a
    FIFO keeps no content).
    """

    POLL_S, DEADLINE_S, GRACE_S = 0.001, 30.0, 2.0
    HOLDER_WAIT_S = 0.2  # how long a holder scan keeps rescanning before it settles for naming no holder
    CONTROL_WINDOW_S = 0.2  # how far either side of an input open with no named holder a control open reaches
    PROC_ROOT = "/proc"  # an instance attribute points a test's scan at a scratch tree of the same shape

    def __init__(self, base):
        self.base, seat = base, base / "root" / ".claude" / "worktrees" / "probe-seat"
        seat.mkdir(parents=True)
        self.input, self.output, self.new_output = seat / "ledger.tsv", seat / "out.txt", seat / "new" / "out.txt"
        self.control = seat / ".probe-control"  # a FIFO beside the input that the lever has no reason to touch (U625)
        self.reads, self.errors, self.replaced, self.attempts = [], [], [], 0
        self.scanner_opens = []  # input opens with no named holder and a control open in their window: no failure
        self._pending, self._control_opens = [], []  # input opens awaiting _settle; (attempt, clock) of control opens
        os.mkfifo(self.input, 0o600)
        os.mkfifo(self.control, 0o600)
        self.output.write_text(LEGIT)
        os.utime(self.output, ns=(BASELINE_NS, BASELINE_NS))
        self._identity = {path: (os.lstat(path).st_ino, os.lstat(path).st_mode) for path in (self.input, self.output)}
        st = os.lstat(self.input)
        self._dev_ino = (st.st_dev, st.st_ino)  # what os.stat of a /proc descriptor link reports for a holder
        self._control_ino = os.lstat(self.control).st_ino
        self._self_test()

    def _open_writer(self, path=None):
        """One write-open attempt on PATH, the input by default: a descriptor when a reader holds it, None when none
        does (ENXIO)."""
        try:
            return os.open(self.input if path is None else path, os.O_WRONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
        except OSError as error:
            if error.errno == errno.ENXIO:
                return None
            raise

    def _self_test(self):
        """Synchronous, on the input and then on the control: no reader means ENXIO; the probe's own reader makes the
        write-open succeed on this very FIFO; closing it brings ENXIO back. Any other answer refuses the probe, since
        reads would not be seen (a control whose reads went unseen would lay a scanner's open on the lever)."""
        self._fifo_self_test(self.input, self._open_writer, self._identity[self.input][0])
        self._fifo_self_test(self.control, functools.partial(self._open_writer, self.control), self._control_ino)

    def _fifo_self_test(self, path, open_writer, inode):
        if (fd := open_writer()) is not None:
            os.close(fd)
            raise RuntimeError(f"{path} has a reader before the consumer ran")
        reader = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
        try:
            writer = open_writer()
            if writer is None:
                raise RuntimeError(f"a reader of {path} did not make the write-open succeed")
            try:
                st = os.fstat(writer)
                if not (stat.S_ISFIFO(st.st_mode) and st.st_ino == inode):
                    raise RuntimeError(f"the write-open of {path} reached another file")
            finally:
                os.close(writer)
        finally:
            os.close(reader)
        if (fd := open_writer()) is not None:
            os.close(fd)
            raise RuntimeError(f"{path} still has a reader after the self-test closed its own")

    def _not_sentinel(self, error=None, fd=None):
        """Whether the input is not the probe's FIFO at this poll, recorded, so the check fails even if the FIFO is
        back by then (a swap and restore between two polls is out of scope). ENOENT is a removal and ELOOP a link
        put in its place."""
        if error is not None:
            if error.errno in (errno.ENOENT, errno.ELOOP):
                self.replaced.append(f"{self.input} was {'removed' if error.errno == errno.ENOENT else 'a link'}")
                return True
            raise error
        st = os.fstat(fd)
        if stat.S_ISFIFO(st.st_mode) and st.st_ino == self._identity[self.input][0]:
            return False
        self.replaced.append(f"{self.input} was another file (inode {st.st_ino}, mode {stat.filemode(st.st_mode)})")
        return True

    def _holders(self, writer):
        """Who holds the input open now, from /proc on Linux: `by pid P (comm, ppid Q: cmdline)` for each process
        whose descriptor table this user can read and that has a descriptor on the sentinel, other than WRITER (the
        probe's own write descriptor, open during the scan); otherwise why none is named. os.stat on a
        /proc/<pid>/fd/<n> link follows it to the open file without opening it, so the scan itself never opens the
        sentinel (a scan that did would record its own read). Every read of the tree tolerates OSError as a class,
        because a pid that exits between its fd listing and its field reads answers ESRCH from /proc and a scan that
        let that escape would abort the attempt and lose the read it had already detected; a holder whose fields are
        gone is still named by its pid. A scan that names nobody is repeated every POLL_S for HOLDER_WAIT_S before
        its answer stands, because a reader the write-open just woke has no descriptor until its `open()` returns
        (the kernel counts it as a reader before that), so the first scan can look before the entry exists."""
        return self._attribution(writer)[0]

    def _attribution(self, writer):
        """The record of _holders and whether it names a holder (False once the scan settled on nobody, or when the
        tree cannot be listed at all); _record_read decides on the second."""
        root = self.PROC_ROOT
        me = str(os.getpid())

        def field(pid, name):
            """One /proc field, `?` when it cannot be read: gone, unreadable, or ESRCH from a pid now exiting."""
            try:
                return Path(root, pid, name).read_bytes().decode(errors="replace")
            except OSError:
                return "?"

        def scan():
            """One pass over the tree: the record when it names a holder, else the no-holder or no-root record."""
            try:
                entries = os.listdir(root)
            except OSError:
                return f"reader not identified (no {root})", False
            holders, unreadable = [], 0
            for pid in entries:
                if not pid.isdigit():
                    continue
                try:
                    descriptors = os.listdir(os.path.join(root, pid, "fd"))
                except PermissionError:  # another user's process (or one not dumpable)
                    unreadable += 1
                    continue
                except OSError:  # exited mid-scan, or an entry that is no descriptor table
                    continue
                for n in descriptors:
                    if pid == me and n == str(writer):
                        continue
                    try:
                        st = os.stat(os.path.join(root, pid, "fd", n))
                    except OSError:  # closed mid-scan, or a descriptor whose target no stat describes
                        continue
                    if (st.st_dev, st.st_ino) != self._dev_ino:
                        continue
                    status = (line for line in field(pid, "status").splitlines() if line.startswith("PPid:"))
                    ppid = next((line.split(":", 1)[1].strip() for line in status), "?")
                    cmdline = field(pid, "cmdline").replace("\0", " ")[:200]
                    holders.append(f"by pid {pid} ({field(pid, 'comm').strip()}, ppid {ppid}: {cmdline})")
                    break
            if holders:
                return ", ".join(holders), True
            return f"by no process whose descriptors this user can read ({unreadable} unreadable)", False

        settle = time.monotonic() + self.HOLDER_WAIT_S
        while True:
            record, named = scan()
            if named or time.monotonic() >= settle:
                return record, named
            time.sleep(self.POLL_S)

    def _record_read(self, writer):
        """One detected open of the sentinel. A named holder is the consumer's read at once. An open with no named
        holder (the scan settled on nobody, or no tree could name one) waits in `_pending` with the clocks of its
        window, the write-open that detected it and the end of the holder scan (the writer closes right after that,
        and a reader that waited for EOF moves on only then); _settle attributes it once the window has closed."""
        opened = time.monotonic()
        record, named = self._attribution(writer)
        if named:
            self.reads.append(f"{self.input} opened for reading {record}")
            return
        when = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self._pending.append((self.attempts, record, when, opened, time.monotonic()))

    def _note_control(self):
        """Whether the control FIFO has a reader now, by the input's own test (a non-blocking write-open that does
        not fail with ENXIO): the attempt and the clock go to `_control_opens`, and the descriptor is closed, which
        gives the reader EOF. A write-open that fails otherwise, or reaches another file, is recorded once as an
        error: a control that is gone cannot tell a scanner from the lever, so the check fails closed."""
        try:
            fd = self._open_writer(self.control)
        except OSError as error:
            entry = f"cannot tell whether {self.control} is being read: {error!r}"
            self.errors += [] if entry in self.errors else [entry]
            return
        if fd is None:
            return
        try:
            st = os.fstat(fd)
            if stat.S_ISFIFO(st.st_mode) and st.st_ino == self._control_ino:
                self._control_opens.append((self.attempts, time.monotonic()))
                return
            entry = f"{self.control} was another file (inode {st.st_ino}, mode {stat.filemode(st.st_mode)})"
            self.errors += [] if entry in self.errors else [entry]
        finally:
            os.close(fd)

    def _control_opens_inside(self, opened, released):
        """The attempts at which the control had a reader inside the window of an input open detected at the clock
        OPENED whose holder scan ended at RELEASED: CONTROL_WINDOW_S either side."""
        first, last = opened - self.CONTROL_WINDOW_S, released + self.CONTROL_WINDOW_S
        return [attempt for attempt, at in self._control_opens if first <= at <= last]

    def _settle(self):
        """Attribute every input open still waiting. The control is watched until the last window has closed (or a
        control open lies inside every window), then an open with a control open inside its window is a scanner's:
        the record names both, goes to `scanner_opens` and is printed on stderr as `worker root: scanner open: ...`,
        no failure; any other is the consumer's read, the pre-U625 record with `(control silent)` before it, and
        assert_untouched fails on it (the class docstring's rule)."""
        while self._pending:
            silent = [p for p in self._pending if not self._control_opens_inside(p[3], p[4])]
            remaining = max((p[4] for p in silent), default=0.0) + self.CONTROL_WINDOW_S - time.monotonic()
            if not silent or remaining <= 0:
                break
            self._note_control()
            time.sleep(min(self.POLL_S, remaining))
        for attempt, record, when, opened, released in self._pending:
            if control := self._control_opens_inside(opened, released):
                entry = f"{self.input} opened for reading {record}, and {self.control} opened for reading inside its"
                entry += f" window at {when} (attempt {attempt}; control at attempt {', '.join(map(str, control))})"
                self.scanner_opens.append(entry)
                print(f"worker root: scanner open: {entry}", file=sys.stderr, flush=True)
            else:
                self.reads.append(f"{self.input} (control silent) opened for reading {record}")
        self._pending = []

    def _attempt(self):
        """One attempt while the consumer runs: note a reader of the control, record a reader of the input, then
        release any writer waiting for a reader."""
        self.attempts += 1
        self._note_control()
        try:
            fd = self._open_writer()
        except OSError as error:
            if error.errno not in (errno.ENOENT, errno.ELOOP):
                self.errors.append(f"cannot tell whether {self.input} is being read: {error!r}")
                return
            self._not_sentinel(error=error)
            return
        if fd is not None:
            try:
                if not self._not_sentinel(fd=fd):
                    self._record_read(fd)
            finally:
                os.close(fd)  # the reader now sees EOF
        try:
            fd = os.open(self.input, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
        except OSError as error:
            if error.errno not in (errno.ENOENT, errno.ELOOP):
                self.errors.append(f"cannot release a writer of {self.input}: {error!r}")
                return
            self._not_sentinel(error=error)
            return
        try:
            self._not_sentinel(fd=fd)
        finally:
            os.close(fd)  # a writer blocked on the open is released; nothing is read from the sentinel

    def consume(self, target, deadline=None):
        """Run the consumer step TARGET in a worker thread while observing the input; return its result or raise
        its exception. A step still running GRACE_S after DEADLINE seconds fails with AssertionError ("consumer
        thread still running after the deadline"); the thread itself is left running (it cannot be stopped). After
        the last attempt the input opens with no named holder are settled (_settle: at most CONTROL_WINDOW_S)."""
        outcome = {}
        worker = threading.Thread(target=lambda: outcome.update(value=target()), name="consumer", daemon=True)
        _CONSUMER_ERRORS[worker] = outcome
        try:
            end = time.monotonic() + (self.DEADLINE_S if deadline is None else deadline)
            worker.start()
            while worker.is_alive():
                if time.monotonic() > end:
                    # Python cannot stop a thread: release a reader blocked on the sentinel, give it a short grace,
                    # and fail if it is still running (nothing is claimed about cleaning it up).
                    self._attempt()
                    worker.join(self.GRACE_S)
                    if worker.is_alive():
                        raise AssertionError("worker root: consumer thread still running after the deadline")
                    break
                self._attempt()
                worker.join(self.POLL_S)
            self._attempt()
            self._settle()
        finally:
            _CONSUMER_ERRORS.pop(worker, None)
        if "error" in outcome:
            raise outcome["error"]
        return outcome.get("value")

    def assert_untouched(self):
        """Nothing opened the input for reading during consume(), or replaced or removed it; nothing wrote, replaced
        or removed the output, or created the new output's directory. The output's content is compared too, since a
        write in place can keep the inode, the size and a coarse clock's mtime. An open in `scanner_opens` is no
        failure (the class docstring's attribution rule); it stays readable there and was printed when settled."""
        self._settle()
        found = []
        for path, identity in self._identity.items():
            if not os.path.lexists(path):
                found.append(f"removed {path}")
                continue
            st = os.lstat(path)
            if path == self.input:
                found += [] if (st.st_ino, st.st_mode) == identity else [f"wrote {path} (replaced)"]
                continue
            content = path.read_bytes() if (st.st_ino, st.st_mode) == identity else b""  # the same regular file only
            if ((st.st_ino, st.st_mode), st.st_mtime_ns, content) != (identity, BASELINE_NS, LEGIT.encode()):
                found.append(f"wrote {path}")
        found += [f"created {self.new_output}"] if self.new_output.parent.exists() else []
        found += [f"wrote {entry} (replaced)" for entry in self.replaced]
        found = [f"read {entry}" for entry in self.reads] + found + self.errors
        if found:
            raise AssertionError("worker root: " + "; ".join(found))


class SwappedFile:
    """A checked file, swap() linking its name (or its stat-measured case alias) to attacker content mid-consumption."""

    def __init__(self, base):
        self.base, self.path, self.attacker = base, base / "Checked.tsv", base / "attacker.tsv"
        self.path.write_text(LEGIT)
        self.attacker.write_text(ATTACKER)
        self.expected_sha = hashlib.sha256(LEGIT.encode()).hexdigest()
        flipped = self.path.with_name(self.path.name.swapcase())
        same = flipped.exists() and os.path.samefile(flipped, self.path)
        self.alias = flipped if same else None
        self.alias_reason = "" if same else f"case-sensitive filesystem under {base}: {flipped.name} does not resolve"

    def swap(self, via_alias=False):
        if (target := self.alias if via_alias else self.path) is None:
            raise RuntimeError(self.alias_reason)
        os.symlink(self.attacker, self.base / ".swap")
        os.replace(self.base / ".swap", target)

    def assert_not_consumed(self, data):
        if not os.path.islink(self.path):  # only swap() makes the checked name a link
            raise AssertionError("never swapped: the consumer did not reach the barrier, so the probe proves nothing")
        if data != LEGIT.encode():
            raise AssertionError("attacker content consumed" if data == ATTACKER.encode() else f"unexpected {data!r}")


@contextlib.contextmanager
def _probe(cls, *args):
    base = Path(tempfile.mkdtemp(prefix="trusted-exec-")).resolve()
    probe = None
    try:
        probe = cls(base, *args)
        yield probe
    finally:
        shutil.rmtree(base, ignore_errors=True)


shim_path = functools.partial(_probe, ShimProbe)  # shim_path(env=None)
hostile_git = functools.partial(_probe, HostileGit)
worker_root = functools.partial(_probe, WorkerRoot)
swapped_file = functools.partial(_probe, SwappedFile)


def parse_env(data):
    """The environment /usr/bin/env -0 printed, as a mapping."""
    return dict(entry.decode().split("=", 1) for entry in data.split(b"\0") if entry)


def assert_sanitized_env(observed, declared=()):
    """The observed names are exactly PATH, HOME, LANG and the consumer's declared names, with PATH=/usr/bin:/bin."""
    want, got, path = set(ALLOWED) | set(declared), set(observed), observed.get("PATH")
    found = [f"missing: {sorted(want - got)}"] if want - got else []
    found += [f"undeclared: {sorted(got - want)}"] if got - want else []
    found += [f"PATH is {path!r}, not {SAFE_PATH!r}"] if path != SAFE_PATH else []
    if found:
        raise AssertionError("environment: " + "; ".join(found))


def repository_root():
    """The checkout this module lives in, from its own path; no Git command or GIT_* variable is consulted."""
    return Path(__file__).resolve().parents[2]


def _directory_service(argv):
    return subprocess.run(argv, env={}, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL).stdout


def passwd_home():
    """The real UID's home from its passwd entry (pwd.getpwuid), never HOME or PATH. dscl (macOS) or getent (Linux)
    cross-checks it when it can run (both seat sandboxes refuse dscl); a disagreeing or malformed answer is refused."""
    entry, darwin = pwd.getpwuid(os.getuid()), sys.platform == "darwin"
    argv = ["/usr/bin/getent", "passwd", str(os.getuid())] if sys.platform.startswith("linux") else None
    argv = ["/usr/bin/dscl", ".", "-read", "/Users/" + entry.pw_name, "NFSHomeDirectory"] if darwin else argv
    try:
        out = _directory_service(argv) if argv else None
    except (OSError, subprocess.CalledProcessError):
        out = None  # the cross-check cannot run here; the passwd entry stands alone
    if out is not None:
        f, dscl = out.rstrip("\n").split(":"), (out.partition(NFS)[2] if out.startswith(NFS) else "").strip()
        other = dscl if darwin else (f[5] if len(f) == 7 else "")
        if other != entry.pw_dir:
            raise RuntimeError(f"the directory service and the passwd entry disagree: {other!r}, {entry.pw_dir!r}")
    if not entry.pw_dir.startswith("/") or "\n" in entry.pw_dir:
        raise RuntimeError(f"no absolute passwd home: {entry.pw_dir!r}")
    return entry.pw_dir


def run_under_trusted_parent(script, *args):
    """Run a regular file inside the repository root under env -i and bash -p, each argument one argument."""
    if not Path(script).is_absolute():
        raise TrustedExecRefused(f"{script}: not an absolute path")
    root, real = repository_root().resolve(), Path(script).resolve()
    if not real.is_relative_to(root):
        raise TrustedExecRefused(f"{script}: resolves to {real}, outside {root}")
    if not real.is_file():  # resolved, so a regular file and not a link to one
        raise TrustedExecRefused(f"{script}: not a regular file")
    argv = ["/usr/bin/env", "-i", f"PATH={SAFE_PATH}", f"HOME={passwd_home()}", "LANG=C.UTF-8"]
    argv += ["/bin/bash", "--noprofile", "--norc", "-p", str(real), *map(str, args)]
    return subprocess.run(argv, env={}, capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL)


class TrustedExecContractMixin:
    """For unittest.TestCase: enter() keeps a context manager until the test ends (enterContext needs Python 3.11)."""

    def enter(self, factory, *args, **kwargs):
        manager = factory(*args, **kwargs)
        value = manager.__enter__()
        self.addCleanup(manager.__exit__, None, None, None)
        return value

    shim_probe = functools.partialmethod(enter, shim_path)
    hostile_git_probe = functools.partialmethod(enter, hostile_git)
    worker_root_probe = functools.partialmethod(enter, worker_root)
    swapped_file_probe = functools.partialmethod(enter, swapped_file)
