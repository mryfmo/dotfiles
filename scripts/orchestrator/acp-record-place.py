#!/usr/bin/env -S python3 -I
"""Place one connection's exit record in the broker directory through one held directory descriptor, or refuse
(regime-cutover U343h).

`acp-record-place.py <broker-dir> <dev>:<ino> <id>`, the record's lines on stdin, is the one writer of `acp-broker`'s
exit record `<seats-root>/.state/<router seat>/broker/<id>`: the connection's reaper runs it, once for the record's
running form and once for its final form, as `python3 -I -S` over a private copy held to the `claude.levers.sha256`
pin, and reads its status. The round-5 audit of U343 (verdict U343g-8a049561, P1 at acp-broker:1262) found the class
record-path in the reaper's own bash: `printf '%s\\n' "$@" > "${record}.tmp"` opened a path for write inside a
directory the Router's sandbox grants for write (the broker directory lies in the Router's own state slot), the
Router learns `<id>` from the stream's first line, and a symbolic link it planted at `<id>.tmp` made the unsandboxed
reaper overwrite a protected host file; the record's `mv -f` had the same shape. This file is the form the program
retired that premise with for hcom-seat's profile write (`profile-config-place.py`, U310d and U310f): no path under the
broker directory is spelled to the kernel after the directory is open, every entry is named relative to the held
descriptor (`dir_fd`), and the directory itself is held by the identity the listener read once. The steps, in order:

- `id`: `<id>` must match `^acp-[a-z0-9][a-z0-9_-]{0,63}-[0-9]{8}-[0-9]{6}-[0-9]+$` (the broker's slot name), so no
  `/`, no `..` and no name outside the grammar reaches any `os` call; `record`: the bytes on stdin are at most 4096,
  not empty and end with a newline (the record's three lines), read before anything is opened.
- `open-dir`: `<broker-dir>` is opened `O_RDONLY | O_DIRECTORY | O_NOFOLLOW` (a link at the name is ELOOP on Linux
  and ENOTDIR on macOS, either a refusal naming a link); `fstat-dir`: it is a directory whose device and inode are
  the `<dev>:<ino>` the listener read when it made the directory (a directory replaced by another at the name is not
  the one the listener made), owned by this user, with no group or other write bit.
- `unlink-temporary`: `<id>.tmp` is removed relative to the descriptor (ENOENT is absence; an entry the Router
  planted, a link to a host file, a dangling link, a regular file or a FIFO, goes as an entry, its target untouched;
  a directory there cannot be unlinked and refuses); `create-temporary`: `<id>.tmp` is created relative to the
  descriptor with `O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW`, mode 0600, so an entry that appeared again between the
  two calls is EEXIST and refuses without the name being opened; `fstat-temporary`: the new descriptor is a regular
  file of this user with one link; `write-temporary`, `fsync-temporary`, then the descriptor is closed.
- `rename`: `os.rename("<id>.tmp", "<id>", src_dir_fd, dst_dir_fd)` with both descriptors the held one: one atomic
  step, so a reader sees the earlier form or the new one whole; a link at `<id>` (to a file or to a directory, where
  `mv -f` would have moved the temporary into that directory) is replaced as an entry and never followed; a directory
  at `<id>` is EISDIR and fails. `fsync-directory`: the directory descriptor is flushed.
- On any failure after the create and before the rename, `unlink-temporary` removes the temporary through the
  descriptor; its own failure is reported in the same line, naming the path that remains.

Exit 0 with nothing on stdout (the reaper's stdout is the connection; nothing of this file's reaches it). Exit 2
refused, one line on stderr naming the step, the path and the reason, nothing created (`id`, `record`, `open-dir`,
`fstat-dir`, `unlink-temporary`, `create-temporary`). Exit 1 a usage error, or a failure after the create
(`fstat-temporary`, `write-temporary`, `fsync-temporary`, `rename`, `fsync-directory`), one line on stderr, the
temporary unlinked. The file imports `errno`, `os`, `re`, `stat` and `sys` only, reads only its arguments and stdin, and
runs under `-I -S`. It is shipped and pinned like the levers (`scripts/generate-agent-configs.py` writes the
byte-identical `home/dot_local/bin/common/executable_acp-record-place.py` and the `claude.levers.sha256` pin, which
the broker's reaper checks on its private copy before each run); `tests/unit/test_acp_record_place.py` holds every
step, every planted entry and every injected failure, and `tests/unit/test_acp_broker.py` the broker's use of it.
"""

import errno
import os
import re
import stat
import sys

NAME = "acp-record-place"
USAGE = f"usage: {NAME}.py <broker-dir> <dev>:<ino> <id>  (the record's lines on stdin)"
GRAMMAR = "^acp-[a-z0-9][a-z0-9_-]{0,63}-[0-9]{8}-[0-9]{6}-[0-9]+$"
RECORD_ID = re.compile(r"acp-[a-z0-9][a-z0-9_-]{0,63}-[0-9]{8}-[0-9]{6}-[0-9]+")
IDENTITY = re.compile(r"[0-9]+:[0-9]+")
LIMIT = 4096
INSIDE = "the reaper writes the record inside the broker directory the listener made only"
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
# The exclusive create: an entry of any kind at the name is EEXIST before anything is opened, and no link is followed.
CREATE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC


class Refusal(Exception):
    """A refused placement, before anything was created: the step, the path and the reason, one stderr line (exit 2)."""

    def __init__(self, step: str, path: str, reason: str) -> None:
        super().__init__(f"refused at {step}: {path}: {reason}")


class Failure(Exception):
    """A failed placement after the create: the step, the path and the reason, one stderr line (exit 1)."""

    def __init__(self, step: str, path: str, reason: str) -> None:
        super().__init__(f"failed at {step}: {path}: {reason}")
        self.step = step
        self.path = path
        self.reason = reason


def errno_text(error: OSError) -> str:
    """`<strerror> (<ERRNO NAME>)`, the kernel's own words for a failed step."""
    code = errno.errorcode.get(error.errno, str(error.errno)) if error.errno is not None else "no errno"
    return f"{error.strerror or 'failed'} ({code})"


def close_quietly(fd: int) -> None:
    try:
        os.close(fd)
    except OSError:
        pass


def read_record(stdin, path: str) -> bytes:
    """The record's bytes from stdin: at most LIMIT, not empty, newline-terminated; read before anything is opened."""
    try:
        data = stdin.read(LIMIT + 1)
    except OSError as error:
        raise Refusal("record", path, f"cannot read the record from stdin: {errno_text(error)}") from None
    if len(data) > LIMIT:
        raise Refusal("record", path, f"the record on stdin exceeds {LIMIT} bytes")
    if not data:
        raise Refusal("record", path, "the record on stdin is empty")
    if not data.endswith(b"\n"):
        raise Refusal("record", path, "the record on stdin does not end with a newline")
    return data


def open_dir(broker_dir: str, identity: "tuple[int, int]") -> int:
    """The one descriptor every later step runs on: the broker directory itself, the one the listener made (its
    device and inode), a directory of this user nobody else can write."""
    try:
        dfd = os.open(broker_dir, DIRECTORY_FLAGS)
    except OSError as error:
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            raise Refusal("open-dir", broker_dir, f"is a symbolic link or not a directory; {INSIDE}") from None
        raise Refusal("open-dir", broker_dir, f"cannot open it: {errno_text(error)}") from None
    try:
        try:
            info = os.fstat(dfd)
        except OSError as error:
            raise Refusal("fstat-dir", broker_dir, f"cannot read its identity: {errno_text(error)}") from None
        if not stat.S_ISDIR(info.st_mode):
            raise Refusal("fstat-dir", broker_dir, "is not a directory")
        if (info.st_dev, info.st_ino) != identity:
            raise Refusal(
                "fstat-dir",
                broker_dir,
                f"is {info.st_dev}:{info.st_ino}, not the broker directory the listener made "
                f"({identity[0]}:{identity[1]}); {INSIDE}",
            )
        uid = os.getuid()
        if info.st_uid != uid:
            raise Refusal("fstat-dir", broker_dir, f"is owned by uid {info.st_uid}, not {uid}")
        if info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
            mode = oct(stat.S_IMODE(info.st_mode))
            raise Refusal("fstat-dir", broker_dir, f"is writable by its group or by others (mode {mode}); {INSIDE}")
    except Refusal:
        close_quietly(dfd)
        raise
    return dfd


def unlink_temporary(dfd: int, name: str, path: str) -> None:
    """Remove the entry at the temporary's name relative to the held descriptor; an absent entry is nothing."""
    try:
        os.unlink(name, dir_fd=dfd)
    except OSError as error:
        if error.errno == errno.ENOENT:
            return
        raise Refusal(
            "unlink-temporary", path, f"cannot remove the entry at the temporary name: {errno_text(error)}"
        ) from None


def create_temporary(dfd: int, name: str, path: str) -> int:
    """A fresh 0600 regular file of this user at `<id>.tmp`, created exclusively relative to the held descriptor."""
    try:
        tfd = os.open(name, CREATE_FLAGS, 0o600, dir_fd=dfd)
    except OSError as error:
        if error.errno == errno.EEXIST:
            raise Refusal(
                "create-temporary",
                path,
                "an entry appeared at the temporary name after its removal; nothing was opened",
            ) from None
        raise Refusal("create-temporary", path, f"cannot create it: {errno_text(error)}") from None
    return tfd


def failed_with_unlink(dfd: int, name: str, path: str, failure: Failure) -> Failure:
    """The temporary removed through the held descriptor after a failure; a removal that fails is named in the line."""
    try:
        os.unlink(name, dir_fd=dfd)
    except OSError as error:
        return Failure(
            failure.step, failure.path, f"{failure.reason}; the temporary {path} remains (unlink: {errno_text(error)})"
        )
    return failure


def write_temporary(tfd: int, data: bytes, path: str) -> None:
    """The record's bytes into the new descriptor, checked as a fresh file of this user first, then flushed."""
    try:
        info = os.fstat(tfd)
    except OSError as error:
        raise Failure("fstat-temporary", path, f"cannot read its identity: {errno_text(error)}") from None
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_nlink != 1:
        raise Failure("fstat-temporary", path, "is not a fresh regular file of this user with one link")
    view = memoryview(data)
    while view:
        try:
            written = os.write(tfd, view)
        except OSError as error:
            raise Failure("write-temporary", path, f"cannot write it: {errno_text(error)}") from None
        view = view[written:]
    try:
        os.fsync(tfd)
    except OSError as error:
        raise Failure("fsync-temporary", path, f"cannot flush it: {errno_text(error)}") from None


def place(broker_dir: str, identity: "tuple[int, int]", record_id: str, data: bytes) -> None:
    """Place `data` as `<id>` inside the broker directory through the held descriptor, or raise Refusal or Failure."""
    name = f"{record_id}.tmp"
    temporary = f"{broker_dir}/{name}"
    record = f"{broker_dir}/{record_id}"
    dfd = open_dir(broker_dir, identity)
    try:
        unlink_temporary(dfd, name, temporary)
        tfd = create_temporary(dfd, name, temporary)
        try:
            try:
                write_temporary(tfd, data, temporary)
            finally:
                close_quietly(tfd)
            try:
                os.rename(name, record_id, src_dir_fd=dfd, dst_dir_fd=dfd)
            except OSError as error:
                if error.errno in (errno.EISDIR, errno.ENOTEMPTY, errno.EEXIST, errno.ENOTDIR):
                    raise Failure("rename", record, f"a directory stands at the record's name; {INSIDE}") from None
                raise Failure("rename", record, f"cannot install it: {errno_text(error)}") from None
        except Failure as failure:
            raise failed_with_unlink(dfd, name, temporary, failure) from None
        try:
            os.fsync(dfd)
        except OSError as error:
            raise Failure("fsync-directory", broker_dir, f"cannot flush the directory: {errno_text(error)}") from None
    finally:
        close_quietly(dfd)


def main(argv: "list[str]", stdin) -> int:
    args = list(argv)
    absolute = len(args) == 3 and args[0].startswith("/")  # lint-comparisons: allow a shape test, no two paths compared
    if len(args) != 3 or not absolute or args[0].startswith("-") or IDENTITY.fullmatch(args[1]) is None:
        print(USAGE, file=sys.stderr)
        return 1
    broker_dir, record_id = args[0].rstrip("/") or "/", args[2]
    dev, ino = args[1].split(":")
    try:
        if RECORD_ID.fullmatch(record_id) is None:
            raise Refusal("id", repr(record_id), f"is outside {GRAMMAR}; no entry is named")
        data = read_record(stdin, f"{broker_dir}/{record_id}")
        place(broker_dir, (int(dev), int(ino)), record_id, data)
    except Refusal as refusal:
        print(f"{NAME}: {refusal}", file=sys.stderr)
        return 2
    except Failure as failure:
        print(f"{NAME}: {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], sys.stdin.buffer))
