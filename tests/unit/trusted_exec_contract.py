"""Shared probes of design-quality 5.14 item 7: one attack each in a temporary fixture, and the trusted parent."""

import contextlib
import errno
import fcntl
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
    from outside the consumer. consume(target) runs the consumer step in a worker thread and, for as long as it
    runs, one sentinel thread stays blocked in `os.open(input, O_WRONLY)`. A blocking write-open of a FIFO returns
    exactly when a reader opens it, however briefly the reader holds it (POSIX; measured on macOS 27 and the kit's
    Ubuntu container at 500 of 500 reader opens that closed again within microseconds), so the blocked thread is a
    latch with no gap: every read open of the input wakes it. On a wake the sentinel records the clock (UTC and
    time.monotonic()), checks by fstat that the descriptor is the probe's own FIFO, runs the holder scan while
    still holding the writer (a reader blocked in read() has its descriptor, and is nameable), closes the writer,
    which gives the reader EOF so it cannot hang, pauses POLL_S (dead time: a reader that still holds the input
    would make the next write-open return at once, and the pause keeps that from spinning) and blocks again. A
    consumer that opens the input for writing blocks in its open until a reader comes, which with the latch in
    place is the teardown's release at the deadline (DEADLINE_S, then GRACE_S): its write then fails (EPIPE) and
    consume() returns, instead of hanging; until round 4 the probe's own non-blocking reader released it within
    POLL_S. Python cannot stop a thread, so a consumer thread still running GRACE_S after the deadline fails
    consume() with "consumer thread still running after the deadline" and nothing is claimed about it. stat()
    opens nothing, so metadata checks never count.

    Why a latch and not a sample. Rounds 3 and 4 of U625 (07efa1d4, b26cbb87) detected an open of either FIFO by a
    non-blocking write-open repeated on a schedule (each attempt, each pass of the holder scan, each poll of the
    settle). The fourth audit (verdicts/U625-3ef4caf7.md, P1 f2 s5, trusted_exec_contract.py:349 at b26cbb87)
    reproduced the gap any sample leaves: one pass over 150 or more /proc entries takes longer than a scanner
    needs to open and close the control, so the control's open fell between two looks and the input's open was
    recorded as the consumer's read (control_closed=True, scanner_opens=0, reads=1). A finer sample moves the gap
    and never closes it; the latch has none, because the kernel wakes the blocked writer for a reader that has
    already closed. The sentinels see opens, not names: a rename of either FIFO wakes nothing, so consume() keeps
    one identity check, `os.lstat` of both names every POLL_S between joins and once more at the teardown, which
    records the input removed, replaced or made a link in `replaced` and the control's in `errors`; a swap put back
    between two checks is out of scope, as before. The teardown releases a blocked sentinel by the probe's own
    `open(fifo, O_RDONLY | O_NONBLOCK)` of the FIFO's second name (release/<name> under the base, a hard link to the
    same inode, so the release reaches the sentinel whatever the consumer did to the name) after setting the
    sentinel's stop flag, and repeats it every POLL_S until the thread has ended, because a sentinel between two
    blocking opens (handling a wake) misses a single release. The sentinel marks a wake it finds the flag set on as
    the teardown's, not a reader's; so before the flag is set the teardown waits until the sentinel holds no write
    descriptor on the FIFO (this process's descriptors, listed through /dev/fd), because the kernel installs that
    descriptor the instant the sentinel's open returns, before the thread runs again: a descriptor present is a
    wake the sentinel has not finished handling, whatever the scheduler did with the thread (the first container
    run of round 5 lost a reader this way, the stop flag set between the kernel's wake and the thread's next
    instruction), and none present is a sentinel still blocked or one between two opens with nothing pending. The
    sentinel is armed before the consumer starts: it signals `armed` from the statement before its open, and
    consume() starts the consumer only after that signal, so on CPython the open has released the interpreter
    lock, which it does on entering the system call, before the consumer runs; what remains is one preemption of
    the sentinel between that release and the system call, inside which a non-blocking reader open that closes
    again is unseen (a blocking one waits for the writer the latch is about to be).

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
    and has a sentinel of its own, latched the same way for the whole of consume(): each wake of it is a reader of
    the control, recorded as a clock in `_control_wakes`, the writer closed at once (the reader gets EOF). An open
    of the input with a named holder is a read, as before. An open with no named holder is a read too, recorded as
    the pre-U625 string with `(control silent)` before it (`<input> (control silent) opened for reading by no
    process whose descriptors this user can read (N unreadable)`), unless the control woke inside the open's
    window: from CONTROL_WINDOW_S before the input's wake to CONTROL_WINDOW_S after its holder scan ended (the
    writer closes right then; a scanner that took the input first reaches the control during the scan or after
    that close, one that took the control first wakes the control's sentinel and then the input's). Then both
    opens are a scanner's: the record names both FIFOs, the unreadable count, the UTC clock of the input's wake
    and each control wake's offset from it, goes to `scanner_opens`, is printed on stderr as `worker root: scanner
    open: ...` so the job log keeps the case, and fails nothing. consume() settles such an open after the input's
    sentinel has stopped, keeping the control's sentinel armed until the last window has closed. The rule is the
    same on a host without /proc (macOS): nothing names a holder there, so every open is a read (`<input> (control
    silent) opened for reading reader not identified (no /proc)`) unless the control woke too. An error in a
    sentinel (its FIFO removed or replaced before a re-arm, or an open failing with anything but the teardown's
    release) is recorded in `errors`, the sentinel ends, and assert_untouched fails: a control the probe cannot
    watch cannot tell a scanner from the lever.

    Left out, what the latch cannot tell: a reader whose open the kernel coalesces with the probe's own release at
    the teardown (between the teardown's last look at the descriptors and its release the stop flag is set, the
    probe records that wake as the teardown's and ignores it, and a reader inside that same wake is unseen; the
    consumer step has ended by then, so such a reader is not the step's own, and at the deadline it is a reader
    that outlived the step); a non-blocking reader open that closes inside the arming preemption named above; a
    second open of the same FIFO inside the POLL_S dead time after a wake (for the input, the first is recorded, so
    the check fails on it anyway; for the control, the first wake lies in every window the second would, short of
    the window's edge by under a millisecond); a scanner that opens only files whose names it knows (the input
    alone, never the control) is reported as the lever's read with the control's silence in the record, so the log
    shows the case; a scanner of this user is named by the scan and reported as a read, as before; and on a host
    without /proc a read the lever made while a scanner happened to open the control passes, since no holder can be
    named there (no macOS host has opened a FIFO of the probe so far).

    Scope. The probe detects any read open of the input during the consumer step, and a replacement or removal of
    the input that is present at an identity check or at the final check. The consumer under test is repository
    code reviewed in the same PR, and the probe guards against an accidental read, not against an adversary inside
    the test process. So it does not claim to detect (residual): a replacement swapped in and restored between two
    identity checks (about a millisecond apart); reads made by audit hooks or other callbacks running inside the
    probe's own calls; a write to the input in place (a FIFO keeps no content).
    """

    POLL_S, DEADLINE_S, GRACE_S = (
        0.001,
        30.0,
        2.0,
    )  # POLL_S: the join and identity-check interval, a sentinel's dead time
    HOLDER_WAIT_S = 0.2  # how long a holder scan keeps rescanning before it settles for naming no holder
    CONTROL_WINDOW_S = 0.2  # how far either side of an input open with no named holder a control open reaches
    PROC_ROOT = "/proc"  # an instance attribute points a test's scan at a scratch tree of the same shape

    def __init__(self, base):
        self.base, seat = base, base / "root" / ".claude" / "worktrees" / "probe-seat"
        seat.mkdir(parents=True)
        self.input, self.output, self.new_output = seat / "ledger.tsv", seat / "out.txt", seat / "new" / "out.txt"
        self.control = seat / ".probe-control"  # a FIFO beside the input that the lever has no reason to touch (U625)
        self.reads, self.errors, self.replaced, self.checks = [], [], [], 0
        self.scanner_opens = []  # input opens with no named holder and a control open in their window: no failure
        self._pending, self._control_wakes = [], []  # input wakes awaiting _settle; monotonic clocks of control wakes
        self._sentinels = {}  # FIFO -> (thread, stop flag) while consume() runs
        os.mkfifo(self.input, 0o600)
        os.mkfifo(self.control, 0o600)
        (base / "release").mkdir()
        self._release = {fifo: base / "release" / fifo.name for fifo in (self.input, self.control)}
        for fifo, alias in self._release.items():
            os.link(fifo, alias)  # a second name of the same inode: the teardown's release reaches a blocked sentinel
        self.output.write_text(LEGIT)
        os.utime(self.output, ns=(BASELINE_NS, BASELINE_NS))
        self._identity = {path: (os.lstat(path).st_ino, os.lstat(path).st_mode) for path in (self.input, self.output)}
        self._dev_inos = {fifo: (os.lstat(fifo).st_dev, os.lstat(fifo).st_ino) for fifo in (self.input, self.control)}
        self._dev_ino = self._dev_inos[self.input]  # what os.stat of a /proc descriptor link reports for a holder
        self._control_ino = self._dev_inos[self.control][1]
        self._self_test()

    def _open_writer(self, path=None):
        """One non-blocking write-open of PATH, the input by default: a descriptor when a reader holds it, None when
        none does (ENXIO). The self-test's probe of the FIFO (and a test's); consume() itself blocks instead."""
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

    def _note_error(self, entry):
        """One line of `errors`, once: the sentinels and the identity check repeat, the record does not."""
        if entry not in self.errors:
            self.errors.append(entry)

    def _not_sentinel(self, st):
        """Whether ST (an lstat of the input's name, or an fstat of the descriptor its sentinel opened) is not the
        probe's FIFO, recorded in `replaced` when so, so the check fails even if the FIFO is back by then."""
        if stat.S_ISFIFO(st.st_mode) and st.st_ino == self._identity[self.input][0]:
            return False
        kind = (
            "a link"
            if stat.S_ISLNK(st.st_mode)
            else f"another file (inode {st.st_ino}, mode {stat.filemode(st.st_mode)})"
        )
        self.replaced.append(f"{self.input} was {kind}")
        return True

    def _check_identity(self):
        """Both names by os.lstat, which opens nothing (so no sentinel wakes): the input removed, a link or another
        file goes to `replaced`; the control's to `errors` once, since a control the probe cannot see cannot tell a
        scanner from the lever. Every POLL_S between consume()'s joins and once more at the teardown: the sentinels
        see opens, never names, so a rename is seen here or not at all."""
        self.checks += 1
        try:
            self._not_sentinel(os.lstat(self.input))
        except FileNotFoundError:
            self.replaced.append(f"{self.input} was removed")
        except OSError as error:
            self._note_error(f"cannot tell whether {self.input} is being read: {error!r}")
        try:
            st = os.lstat(self.control)
        except OSError as error:
            self._note_error(f"cannot tell whether {self.control} is being read: {error!r}")
            return
        if not (stat.S_ISFIFO(st.st_mode) and st.st_ino == self._control_ino):
            self._note_error(f"{self.control} was another file (inode {st.st_ino}, mode {stat.filemode(st.st_mode)})")

    def _holders(self, writer):
        """Who holds the input open now, from /proc on Linux: `by pid P (comm, ppid Q: cmdline)` for each process
        whose descriptor table this user can read and that has a descriptor on the sentinel, other than WRITER (the
        probe's own write descriptor, open during the scan); otherwise why none is named. os.stat on a
        /proc/<pid>/fd/<n> link follows it to the open file without opening it, so the scan itself never opens the
        sentinel (a scan that did would record its own read). Every read of the tree tolerates OSError as a class,
        because a pid that exits between its fd listing and its field reads answers ESRCH from /proc and a scan that
        let that escape would abort the wake and lose the read it had already detected; a holder whose fields are
        gone is still named by its pid. A scan that names nobody is repeated every POLL_S for HOLDER_WAIT_S before
        its answer stands, because a reader the write-open just woke has no descriptor until its `open()` returns
        (the kernel counts it as a reader before that), so the first scan can look before the entry exists. The
        scan runs in the input's sentinel thread while that thread holds its writer; the control's sentinel stays
        latched meanwhile, so a scanner that reaches the control during the scan is seen without the scan looking
        (round 4 sampled the control between two passes, and the verdict of b26cbb87 showed the open that fell
        between them laid on the lever)."""
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

    def _record_read(self, writer, woke, when):
        """One wake of the input's sentinel at the clocks WOKE (monotonic) and WHEN (UTC), WRITER its descriptor. A
        named holder is the consumer's read at once. An open with no named holder (the scan settled on nobody, or
        no tree could name one) waits in `_pending` with the clocks of its window, the wake and the end of the
        holder scan (the writer closes right after that, and a reader that waited for EOF moves on only then);
        _settle attributes it once the window has closed."""
        record, named = self._attribution(writer)
        if named:
            self.reads.append(f"{self.input} opened for reading {record}")
            return
        self._pending.append((record, when, woke, time.monotonic()))

    def _sentinel(self, fifo, woke, armed, stopping):
        """The latch on FIFO, in a thread of its own for the whole of consume(): signal ARMED, block in a write-open
        until a reader opens, hand the wake to WOKE (the descriptor and both clocks; False from it ends the latch),
        close the writer (a reader blocked in read() gets EOF), pause POLL_S (the dead time) and block again, until
        STOPPING is set. The teardown's release is a wake too: STOPPING is set before it opens, so a wake that finds
        it set is the teardown's and is not handed on. An open that fails (ENOENT: the FIFO removed before a
        re-arm; ELOOP: a link in its place; anything else) is recorded in `errors` and ends the latch, so the check
        fails closed; so is any other failure of the thread, before the thread's hook reports it."""
        try:
            while not stopping.is_set():
                armed.set()
                try:
                    fd = os.open(fifo, os.O_WRONLY | os.O_NOFOLLOW)
                except OSError as error:
                    self._note_error(f"cannot tell whether {fifo} is being read: {error!r}")
                    return
                clocks = time.monotonic(), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                try:
                    if stopping.is_set() or not woke(fd, *clocks):
                        return
                finally:
                    os.close(fd)
                time.sleep(self.POLL_S)
        except Exception as error:
            self._note_error(f"the sentinel of {fifo} failed: {error!r}")
            raise

    def _input_woke(self, fd, woke, when):
        """A reader opened the input: a descriptor on another file (the name swapped before this re-arm) is a
        replacement and ends the latch; else the holder scan runs while FD is held, and the open is recorded."""
        if self._not_sentinel(os.fstat(fd)):
            return False
        self._record_read(fd, woke, when)
        return True

    def _control_woke(self, fd, woke, when):
        """A reader opened the control: the clock goes to `_control_wakes`; a descriptor on another file is an error
        (the control cannot be watched) and ends the latch."""
        st = os.fstat(fd)
        if stat.S_ISFIFO(st.st_mode) and st.st_ino == self._control_ino:
            self._control_wakes.append(woke)
            return True
        self._note_error(f"{self.control} was another file (inode {st.st_ino}, mode {stat.filemode(st.st_mode)})")
        return False

    def _start_sentinel(self, fifo, woke):
        """Start the latch on FIFO and return once it is armed (the class docstring: the signal comes from the
        statement before the blocking open, and the consumer is started only after it)."""
        armed, stopping = threading.Event(), threading.Event()
        name = f"sentinel {fifo.name}"
        thread = threading.Thread(target=self._sentinel, args=(fifo, woke, armed, stopping), name=name, daemon=True)
        self._sentinels[fifo] = (thread, stopping)
        thread.start()
        while not armed.wait(self.GRACE_S):
            if not thread.is_alive():  # the open failed at once: the error is recorded, nothing to arm
                return

    def _holds_writer(self, fifo):
        """Whether this process holds a write descriptor on FIFO, from /dev/fd (this process's descriptors on both
        platforms): the kernel installs the sentinel's descriptor the instant its open returns, before the thread
        runs again, so this tells a wake the sentinel has not yet handled from a sentinel still blocked."""
        for name in os.listdir("/dev/fd"):
            try:
                fd = int(name)
                st = os.fstat(fd)
                if (st.st_dev, st.st_ino) != self._dev_inos[fifo]:
                    continue
                if fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_ACCMODE == os.O_WRONLY:
                    return True
            except (ValueError, OSError):  # not a descriptor number, or one closed meanwhile
                continue
        return False

    def _stop_sentinel(self, fifo):
        """End the latch on FIFO. First wait, every POLL_S for at most GRACE_S, until this process holds no write
        descriptor on the FIFO (_holds_writer: a wake the sentinel has not finished handling; one that outlasts the
        grace is recorded as an error). Then set the stop flag, open and close a non-blocking reader of the FIFO's
        second name (release/<name>, the same inode whatever the consumer did to the name), which wakes a sentinel
        blocked in its write-open and any consumer blocked in a write-open of the input, and repeat every POLL_S
        until the thread has ended, since a sentinel between two blocking opens misses a single release.
        Idempotent."""
        if (sentinel := self._sentinels.pop(fifo, None)) is None:
            return
        thread, stopping = sentinel
        settle = time.monotonic() + self.GRACE_S
        while thread.is_alive() and self._holds_writer(fifo):
            if time.monotonic() > settle:
                self._note_error(f"the sentinel of {fifo} did not finish handling a wake within {self.GRACE_S} s")
                break
            time.sleep(self.POLL_S)
        stopping.set()
        while thread.is_alive():
            os.close(os.open(self._release[fifo], os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW))
            thread.join(self.POLL_S)

    def _control_wakes_inside(self, opened, released):
        """The clocks at which the control woke inside the window of an input wake at the clock OPENED whose holder
        scan ended at RELEASED: CONTROL_WINDOW_S either side."""
        first, last = opened - self.CONTROL_WINDOW_S, released + self.CONTROL_WINDOW_S
        return [at for at in self._control_wakes if first <= at <= last]

    def _settle(self):
        """Attribute every input wake still waiting, once the control can have nothing more to say about it: the
        control's sentinel stays latched until CONTROL_WINDOW_S after the last silent wake's scan ended (nothing to
        wait for when a control wake lies inside every window), then ends. Then a wake with a control wake inside
        its window is a scanner's: the record names both, with each control wake's offset from the input's, goes
        to `scanner_opens` and is printed on stderr as `worker root: scanner open: ...`, no failure; any other is
        the consumer's read, the pre-U625 record with `(control silent)` before it, and assert_untouched fails on
        it (the class docstring's rule). Idempotent: consume() settles its own wakes."""
        silent = [
            released for _, _, opened, released in self._pending if not self._control_wakes_inside(opened, released)
        ]
        if silent and (remaining := max(silent) + self.CONTROL_WINDOW_S - time.monotonic()) > 0:
            time.sleep(remaining)
        self._stop_sentinel(self.control)
        for record, when, opened, released in self._pending:
            if wakes := self._control_wakes_inside(opened, released):
                offsets = ", ".join(f"{at - opened:+.3f} s" for at in wakes)
                entry = f"{self.input} opened for reading {record}, and {self.control} opened for reading inside its"
                entry += f" window at {when} (control woke {offsets} from the input's wake)"
                self.scanner_opens.append(entry)
                print(f"worker root: scanner open: {entry}", file=sys.stderr, flush=True)
            else:
                self.reads.append(f"{self.input} (control silent) opened for reading {record}")
        self._pending = []

    def consume(self, target, deadline=None):
        """Run the consumer step TARGET in a worker thread while observing the input; return its result or raise
        its exception. Both sentinels are armed before the step starts and end after it; the identity check runs
        every POLL_S between joins. A step still running GRACE_S after DEADLINE seconds fails with AssertionError
        ("consumer thread still running after the deadline"); the input's sentinel is released first, which also
        releases a consumer blocked in a write-open of the input; the thread itself is left running (it cannot be
        stopped). After the step the input wakes with no named holder are settled (_settle: at most
        CONTROL_WINDOW_S)."""
        outcome = {}
        worker = threading.Thread(target=lambda: outcome.update(value=target()), name="consumer", daemon=True)
        _CONSUMER_ERRORS[worker] = outcome
        try:
            end = time.monotonic() + (self.DEADLINE_S if deadline is None else deadline)
            self._start_sentinel(self.control, self._control_woke)
            self._start_sentinel(self.input, self._input_woke)
            worker.start()
            while worker.is_alive():
                if time.monotonic() > end:
                    # Python cannot stop a thread: release a writer blocked on the sentinel, give it a short grace,
                    # and fail if it is still running (nothing is claimed about cleaning it up).
                    self._stop_sentinel(self.input)
                    worker.join(self.GRACE_S)
                    if worker.is_alive():
                        raise AssertionError("worker root: consumer thread still running after the deadline")
                    break
                self._check_identity()
                worker.join(self.POLL_S)
            self._check_identity()
        finally:
            self._stop_sentinel(self.input)
            self._settle()
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
