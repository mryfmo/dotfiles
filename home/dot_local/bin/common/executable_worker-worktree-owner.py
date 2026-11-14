#!/usr/bin/env -S python3 -I -S
"""Claim or release a worker tree's owner record under one lock, through one descriptor (regime-cutover U509e).

`worker-worktree.sh claim <unit> <owner> [--stale <minutes>]` and `release <unit> <owner>` (U509, standing order 27:
one writer per tree) run this program and act on its exit status alone: `worker-worktree-owner.py <root> claim <unit>
<owner> [--stale <minutes>]` or `<root> release <unit> <owner>`, the root the lever resolved (`place_root`). Round 1
(verdicts/U509-e343a569.md) kept the record in the shell and found six defects of two classes: the read and the
mutation were separate steps with nothing between them held (two stale claimers both won; a release that had read
its owner before a successor's claim removed the successor's record), and the shell's reads were not the file's
bytes (`$(…)` dropped a NUL, so `owner=W<NUL>1` read as `W1`; `((10#n))` overflowed, so `--stale 9223372036854775808`
went negative and took over an age-zero claim; a day of 31 passed for every month; a failed write after the exclusive
create left an empty record and exit 3). This program is the form `ledger-row.py` (U222) and `profile-config-place.py`
(U310d) take:

- The tree `<root>/<unit>` is opened `O_RDONLY | O_DIRECTORY | O_NOFOLLOW`, then its `.git` through that descriptor
  with the same flags (a link at either name is refused by the open itself, never by a check a swap could follow),
  `fstat`ed as a directory of this user. Every later name (`regime-owner`, the lock, the temporary) is relative to
  the `.git` descriptor (`dir_fd`); no path is walked again after that open.
- One lock: `regime-owner.lock` beside the record, opened `O_CREAT` through the descriptor (mode 0600; it stays,
  since removing a lock file lets a waiter lock a dead inode) and `flock(LOCK_EX)` tried non-blocking every 0.05 s
  for up to 10 s, expiry a refusal. The read, the decision and the write or removal all run under it, so of two
  claimers on one stale record exactly one takes over and the other reads the fresh record and is refused, and a
  release that is delayed past a successor's claim reads the successor's name and is refused.
- The record is read as bytes through the descriptor (`O_NOFOLLOW | O_NONBLOCK`: a link refuses, a FIFO never
  blocks, ENOENT alone is absence) and matched whole: `owner=<name over [A-Za-z0-9._-]{1,64}>\\n` then
  `claimed=<YYYY-MM-DDTHH:MM:SSZ>\\n`, nothing before, between or after, so a NUL or any byte outside the grammar is
  malformed; the stamp is parsed with `strptime` and must print back to the same string (2026-02-31 is refused).
  A malformed record is left in place and named (exit 2); a read that fails is a refusal naming the error, never an
  absence (standing order 21).
- The write, fresh or takeover, is an exclusive temporary `.regime-owner.<16 hex>` created through the descriptor
  (`O_CREAT | O_EXCL | O_NOFOLLOW`, 0600 by `fchmod`), written, `fsync`ed and renamed over `regime-owner` in one
  step; a step that fails removes the temporary and exits 1 with the previous record standing (SIGXFSZ is ignored so
  a file-size limit is EFBIG from `write`, handled, not a death). A release is one `unlink` through the descriptor.
- `--stale` is 1 to 6 decimal digits (at most 999999 minutes), so the age comparison is on small integers; the age
  is `(now - claimed) // 60` in whole minutes, a record from the future at age 0. The clock is `datetime.now(UTC)`.

Exit 0 with one stdout line in the lever's words: `claimed <unit> owner=<name>`, `taken over <unit> from=<old>
age=<min>m owner=<name>`, `released <unit> owner=<name>`, `no claim <unit>`. Exit 3 refused by the record (a live
owner on `claim`, another owner on `release`), exit 2 refused by shape (usage, the grammar, the tree, a malformed or
unreadable record, the lock), exit 1 a write or removal that failed after the decision; every refusal is one stderr
line beginning `worker-worktree.sh: refused: ` (the lever's `refuse`), a failed write `worker-worktree.sh: failed: `.
Every argument must round-trip through strict UTF-8. The program imports `datetime`, `errno`, `fcntl`, `os`, `re`,
`secrets`, `signal`, `stat`, `sys` and `time` only, reads no environment variable and runs under `-I -S`. It is shipped
and pinned like the levers (`scripts/generate-agent-configs.py` writes the byte-identical
`home/dot_local/bin/common/executable_worker-worktree-owner.py` and the `claude.levers.sha256` pin); the lever reads
the file once, hashes those bytes against the pin and runs those same bytes (`python3 -I -S -`), so no path is read
twice between the hash and the run. `tests/unit/test_worker_worktree.py` runs it through the lever.
"""

import errno
import fcntl
import os
import re
import secrets
import signal
import stat
import sys
import time
from datetime import datetime, timezone

LEVER = "worker-worktree.sh"
USAGE = (
    "usage: worker-worktree.sh <unit> <branch> <base> | claim <unit> <owner> [--stale <minutes>] | "
    "release <unit> <owner>"
)
RECORD = "regime-owner"
LOCK = "regime-owner.lock"
TEMPORARY_PREFIX = ".regime-owner."
STALE_DEFAULT = 20
STAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
LOCK_WAIT = 10.0
LOCK_POLL = 0.05
UNIT = re.compile(r"^U[0-9]+[a-z]?$")
OWNER = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
STALE = re.compile(r"^[0-9]{1,6}$")
# The record, matched whole over its bytes: a NUL, a third line, a missing final newline or any byte outside the
# grammar fails the match, so nothing of it is ever read as an owner or a time.
RECORD_BYTES = re.compile(
    rb"owner=([A-Za-z0-9._-]{1,64})\nclaimed=([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)\n"
)
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
READ_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC
LOCK_FLAGS = os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC
CREATE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
CHUNK = 65536


class Refusal(Exception):
    """One stderr line and an exit status: 2 by shape, 3 by the record, 1 a failed write or removal."""

    def __init__(self, status: int, reason: str) -> None:
        super().__init__(reason)
        self.status = status
        self.reason = reason


def refuse(reason: str) -> Refusal:
    return Refusal(2, reason)


def refuse_owned(reason: str) -> Refusal:
    return Refusal(3, reason)


def failed(reason: str) -> Refusal:
    return Refusal(1, reason)


def errno_text(error: OSError) -> str:
    """`<strerror> (<ERRNO NAME>)`, the kernel's own words for a failed step."""
    code = errno.errorcode.get(error.errno, str(error.errno)) if error.errno is not None else "no errno"
    return f"{error.strerror or 'failed'} ({code})"


def close_quietly(fd: int) -> None:
    try:
        os.close(fd)
    except OSError:
        pass


def check_arguments(argv: "list[str]") -> None:
    """Every argument round-trips through strict UTF-8 (Python decodes argv with surrogateescape, so a byte outside
    UTF-8 would otherwise travel into a message or a record)."""
    for argument in argv:
        try:
            argument.encode("utf-8", "strict")
        except UnicodeEncodeError:
            raise refuse("an argument is not UTF-8") from None


def parse(argv: "list[str]") -> "tuple[str, str, str, str, int]":
    """(root, verb, unit, owner, stale) from the lever's arguments, each refused by name outside its grammar."""
    if len(argv) < 4 or argv[1] not in ("claim", "release"):
        raise refuse(USAGE)
    root, verb, unit, owner = argv[0], argv[1], argv[2], argv[3]
    rest = argv[4:]
    stale = STALE_DEFAULT
    if verb == "claim":
        while rest:
            if rest[0] != "--stale":
                raise refuse(USAGE)
            if len(rest) < 2:
                raise refuse("--stale needs a count of minutes")
            if not STALE.match(rest[1]):
                raise refuse(f"--stale {rest[1]} is not a count of minutes of 1 to 6 digits")
            stale = int(rest[1])
            rest = rest[2:]
    elif rest:
        raise refuse(USAGE)
    if not UNIT.match(unit):
        raise refuse(f"the unit {unit} is not U<n> or U<n><letter>")
    if not OWNER.match(owner):
        raise refuse(f"the owner {owner} is not a name over [A-Za-z0-9._-]{{1,64}}")
    if not root.startswith("/"):
        raise refuse(f"the root {root} is not an absolute path")
    return root, verb, unit, owner, stale


def open_git_dir(path: str) -> int:
    """The `.git` directory of the tree `path`, opened through the tree's own descriptor with `O_NOFOLLOW` at each
    of the two names: the open is the check, so no link planted between a check and the open is followed. A
    directory of this user, else refused; the descriptor every later name is relative to."""
    try:
        tfd = os.open(path, DIRECTORY_FLAGS)
    except OSError as error:
        if error.errno == errno.ENOENT:
            raise refuse(
                f"the tree {path} does not exist; make it with worker-worktree.sh <unit> <branch> <base> first"
            ) from None
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            raise refuse(f"the tree {path} is a symbolic link; a worker tree is the directory the lever made") from None
        raise refuse(f"cannot open the tree {path}: {errno_text(error)}") from None
    try:
        try:
            dfd = os.open(".git", DIRECTORY_FLAGS, dir_fd=tfd)
        except OSError as error:
            if error.errno == errno.ELOOP:
                raise refuse(
                    f"{path}/.git is a symbolic link; a worker tree's .git is the directory the lever made"
                ) from None
            if error.errno == errno.ENOTDIR:
                # macOS answers ENOTDIR for a link too; the entry's own kind picks the words, the open was the refusal
                try:
                    kind = os.lstat(".git", dir_fd=tfd)
                except OSError:
                    kind = None
                if kind is not None and stat.S_ISLNK(kind.st_mode):
                    raise refuse(
                        f"{path}/.git is a symbolic link; a worker tree's .git is the directory the lever made"
                    ) from None
                raise refuse(f"{path} is no worker repository: {path}/.git is not a directory") from None
            if error.errno == errno.ENOENT:
                raise refuse(f"{path} is no worker repository: {path}/.git is not a directory") from None
            raise refuse(f"cannot open {path}/.git: {errno_text(error)}") from None
    finally:
        close_quietly(tfd)
    try:
        info = os.fstat(dfd)
    except OSError as error:
        close_quietly(dfd)
        raise refuse(f"cannot read the identity of {path}/.git: {errno_text(error)}") from None
    if not stat.S_ISDIR(info.st_mode):
        close_quietly(dfd)
        raise refuse(f"{path} is no worker repository: {path}/.git is not a directory")
    if info.st_uid != os.geteuid():
        close_quietly(dfd)
        raise refuse(f"{path} is no worker repository: {path}/.git is not this user's")
    return dfd


def take_lock(dfd: int, git_dir: str) -> int:
    """The one lock every record operation runs under: `regime-owner.lock` beside the record, opened through the
    descriptor and `flock`ed exclusively; a wait past LOCK_WAIT seconds refuses naming the file."""
    lock_path = f"{git_dir}/{LOCK}"
    try:
        lfd = os.open(LOCK, LOCK_FLAGS, 0o600, dir_fd=dfd)
    except OSError as error:
        raise refuse(f"cannot open the lock {lock_path}: {errno_text(error)}") from None
    deadline = time.monotonic() + LOCK_WAIT
    while True:
        try:
            fcntl.flock(lfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return lfd
        except OSError as error:
            if error.errno not in (errno.EWOULDBLOCK, errno.EAGAIN):
                close_quietly(lfd)
                raise refuse(f"cannot lock {lock_path}: {errno_text(error)}") from None
        if time.monotonic() >= deadline:
            close_quietly(lfd)
            raise refuse(f"cannot lock {lock_path} within {LOCK_WAIT:g} s; another claim or release holds it")
        time.sleep(LOCK_POLL)


def read_all(fd: int, record_path: str) -> bytes:
    parts = []
    while True:
        try:
            chunk = os.read(fd, CHUNK)
        except OSError as error:
            raise refuse(f"cannot read the owner record {record_path}: {errno_text(error)}") from None
        if not chunk:
            return b"".join(parts)
        parts.append(chunk)


def read_record(dfd: int, record_path: str) -> "tuple[str, str, int] | None":
    """(owner, stamp, epoch seconds) of the record read through the descriptor, None when there is none. The only
    shape read is the two exact lines; anything else refuses and leaves the file for the operator."""
    malformed = (
        f"the owner record {record_path} is not the two lines owner=<name> and claimed=<YYYY-MM-DDTHH:MM:SSZ>; "
        "remove it by hand"
    )
    try:
        rfd = os.open(RECORD, READ_FLAGS, dir_fd=dfd)
    except OSError as error:
        if error.errno == errno.ENOENT:
            return None
        if error.errno == errno.ELOOP:
            raise refuse(f"the owner record {record_path} is a symbolic link; remove it by hand") from None
        raise refuse(f"cannot read the owner record {record_path}: {errno_text(error)}") from None
    try:
        try:
            info = os.fstat(rfd)
        except OSError as error:
            raise refuse(f"cannot read the owner record {record_path}: {errno_text(error)}") from None
        if not stat.S_ISREG(info.st_mode):
            raise refuse(f"the owner record {record_path} is not a regular file; remove it by hand")
        content = read_all(rfd, record_path)
    finally:
        close_quietly(rfd)
    match = RECORD_BYTES.fullmatch(content)
    if match is None:
        raise refuse(malformed)
    owner = match.group(1).decode("ascii")
    stamp = match.group(2).decode("ascii")
    try:
        claimed = datetime.strptime(stamp, STAMP_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError:
        raise refuse(malformed) from None
    if claimed.strftime(STAMP_FORMAT) != stamp:
        raise refuse(malformed)
    return owner, stamp, int(claimed.timestamp())


def write_record(dfd: int, git_dir: str, owner: str, stamp: str) -> None:
    """The record as one exclusive temporary written, synced and renamed over `regime-owner` through the descriptor;
    a step that fails removes the temporary and exits 1, the previous record standing."""
    name = TEMPORARY_PREFIX + secrets.token_hex(8)
    temporary = f"{git_dir}/{name}"
    record_path = f"{git_dir}/{RECORD}"
    try:
        tfd = os.open(name, CREATE_FLAGS, 0o600, dir_fd=dfd)
    except OSError as error:
        raise failed(f"cannot create the temporary {temporary} for the owner record: {errno_text(error)}") from None
    try:
        try:
            os.fchmod(tfd, 0o600)
        except OSError as error:
            raise failed(f"cannot set the mode of {temporary}: {errno_text(error)}") from None
        data = memoryview(f"owner={owner}\nclaimed={stamp}\n".encode("ascii"))
        while data:
            try:
                written = os.write(tfd, data)
            except OSError as error:
                raise failed(f"cannot write the owner record {record_path}: {errno_text(error)}") from None
            data = data[written:]
        try:
            os.fsync(tfd)
        except OSError as error:
            raise failed(f"cannot flush the owner record {record_path}: {errno_text(error)}") from None
        try:
            os.rename(name, RECORD, src_dir_fd=dfd, dst_dir_fd=dfd)
        except OSError as error:
            raise failed(f"cannot replace the owner record {record_path}: {errno_text(error)}") from None
    except Refusal as refusal:
        close_quietly(tfd)
        try:
            os.unlink(name, dir_fd=dfd)
        except OSError as error:
            raise failed(f"{refusal.reason}; the temporary {temporary} remains (unlink: {errno_text(error)})") from None
        raise failed(f"{refusal.reason}; the temporary {temporary} removed, the previous record stands") from None
    close_quietly(tfd)


def claim(dfd: int, path: str, unit: str, owner: str, stale: int) -> str:
    git_dir = f"{path}/.git"
    now = datetime.now(timezone.utc).replace(microsecond=0)
    stamp = now.strftime(STAMP_FORMAT)
    current = read_record(dfd, f"{git_dir}/{RECORD}")
    if current is None:
        write_record(dfd, git_dir, owner, stamp)
        return f"claimed {unit} owner={owner}"
    old_owner, old_stamp, claimed = current
    age = max(0, (int(now.timestamp()) - claimed) // 60)
    if age < stale:
        raise refuse_owned(
            f"the tree {path} is owned by {old_owner} (claimed {old_stamp}, {age} min ago); release it or wait past "
            "--stale"
        )
    write_record(dfd, git_dir, owner, stamp)
    return f"taken over {unit} from={old_owner} age={age}m owner={owner}"


def release(dfd: int, path: str, unit: str, owner: str) -> str:
    git_dir = f"{path}/.git"
    current = read_record(dfd, f"{git_dir}/{RECORD}")
    if current is None:
        return f"no claim {unit}"
    old_owner = current[0]
    if old_owner != owner:
        raise refuse_owned(f"the tree {path} is owned by {old_owner}, not {owner}; only the owner releases it")
    try:
        os.unlink(RECORD, dir_fd=dfd)
    except OSError as error:
        raise failed(f"cannot remove the owner record {git_dir}/{RECORD}: {errno_text(error)}") from None
    return f"released {unit} owner={owner}"


def main(argv: "list[str]") -> int:
    # A file-size limit hit while the record is written is EFBIG from `write`, handled below, not a death by signal.
    signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
    try:
        check_arguments(argv)
        root, verb, unit, owner, stale = parse(argv)
        path = f"{root.rstrip('/') or ''}/{unit}"
        dfd = open_git_dir(path)
        try:
            lfd = take_lock(dfd, f"{path}/.git")
            try:
                line = claim(dfd, path, unit, owner, stale) if verb == "claim" else release(dfd, path, unit, owner)
            finally:
                close_quietly(lfd)
        finally:
            close_quietly(dfd)
    except Refusal as refusal:
        word = "failed" if refusal.status == 1 else "refused"
        print(f"{LEVER}: {word}: {refusal.reason}", file=sys.stderr)
        return refusal.status
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
