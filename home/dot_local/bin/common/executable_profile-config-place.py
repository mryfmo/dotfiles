#!/usr/bin/env -S python3 -I
"""Place a dsh profile's `agent/config.yml` through one held directory descriptor, or refuse (regime-cutover U310d).

`profile-config-place.py [--dry-run] <agent-dir> <uid>`, the rendered config on stdin, is the one writer of the dsh
role's profile config: `scripts/orchestrator/hcom-seat` resolves the profile's `agent/` directory (the dsh row's own
containment judgement, U272 and U306) and runs this file beside it as `python3 -I -S`, reading its status. Three audit
rounds of U310 found one class, symlink-write, in the launcher's bash: each round checked a path and then acted on it,
and a process that owns `agent/` (the role's own sandboxed dsh) swapped the entry between the two. Here no path is
checked and then acted on: every operation on `agent/` runs on one descriptor of the directory itself, opened once
with `O_NOFOLLOW`, and every entry inside it is named relative to that descriptor (`dir_fd`), so no component can be
swapped between a reading and the act that follows it. The steps, in order:

- `open-agent`: `agent-dir` is opened `O_RDONLY | O_DIRECTORY | O_NOFOLLOW` (a link at `agent` is ELOOP on Linux and
  ENOTDIR on macOS, either a refusal naming a link); `fstat-agent`: it is a directory of `uid` whose mode grants no
  group or other write.
- `open-config`: `config.yml` is opened through the descriptor with `O_NOFOLLOW | O_NONBLOCK` (ENOENT is absence; a link
  is ELOOP and refuses); `fstat-config`: a regular file of `uid` (a directory or a FIFO refuses); `read-config`: its
  bytes. Equal to the rendering: `verify-kept`, then `kept`, nothing written. With `--dry-run` the run stops here:
  `absent` or `differs`.
- `create-temporary`: `.config.yml.<16 hex>` (`secrets.token_hex`) is created through the descriptor with
  `O_CREAT | O_EXCL | O_NOFOLLOW` (read-write, so the read-back below runs on this same descriptor), mode 0600, so a
  regular file, a link (dangling too), a FIFO or a directory planted at the name is EEXIST and refuses without the name
  being opened and without blocking; `fstat-temporary`: the new descriptor is a regular file of `uid` with one link, and
  its identity (device, inode) is kept; `fchmod-temporary` 0600; `write-temporary`; `fsync-temporary`.
- `rename`: `os.rename(tmp, "config.yml", src_dir_fd, dst_dir_fd)`: one atomic step; a link at the destination is
  replaced as an entry (its target untouched), a directory there is EISDIR and refuses.
- `verify-placed`: the written descriptor is read back from its start and must hold the rendering; then `config.yml`
  is opened again through the held directory descriptor (`O_NOFOLLOW`) and the identity of that open must be the
  written descriptor's. Another inode at the name (round-4 verdict P2 at :225: a writer that replaced `config.yml`
  during the read-back was reported as `placed`) is read once through the directory descriptor: it must be a regular
  file of `uid` holding the rendering (two launches at once that land the same bytes, the role's normal case) and must
  still be the inode at the name on one more open; anything else refuses, so the launch never reports `placed` while
  the name holds another inode's bytes. `verify-kept` is the same identity check after a compare that found the
  rendering, so a replacement of the entry during that read is never reported as `kept`. What no read-back closes
  (round-5 verdict P2 at :197): a process of the directory's owner, the role's own user (`fstat-agent` admits no
  other writer), may rewrite `config.yml` in place, during a read or at any moment after placement; the kit treats
  that writer as the role itself, and the U310 body carries it as a residual row, not as a guarantee.
- On any refusal after the create and before the rename, `unlink-temporary` removes the temporary through the
  descriptor; its own failure is reported in the same line, naming the path that remains.

Exit 0 with one word on stdout: `placed`, `replaced` or `kept` (`absent`, `differs` or `kept` with `--dry-run`). Exit 2
refused, one line on stderr naming the step, the path and the errno. Exit 1 a usage error. The file imports `errno`,
`os`, `secrets`, `stat` and `sys` only, reads no environment variable and runs under `-I -S`. It is shipped and pinned
like the levers (`scripts/generate-agent-configs.py` writes the byte-identical
`home/dot_local/bin/common/executable_profile-config-place.py` and the `claude.levers.sha256` pin, which hcom-seat
checks before running it); `tests/unit/test_profile_config_place.py` holds every step and every injected failure.
"""

import errno
import os
import secrets
import stat
import sys

NAME = "profile-config-place"
USAGE = f"usage: {NAME}.py [--dry-run] <agent-dir> <uid>  (the rendered config on stdin)"
CONFIG = "config.yml"
TEMPORARY_PREFIX = ".config.yml."
INSIDE = "the dsh role writes its profile config inside its profile only"
# The read-only opens: no link followed at the last component, and no blocking on a FIFO planted at the name.
READ_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
# The exclusive create: an entry of any kind at the name is EEXIST before anything is opened. Read-write, so the
# read-back after the rename runs on this descriptor, the one that wrote the bytes.
CREATE_FLAGS = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC
CHUNK = 65536


class Refusal(Exception):
    """A refused placement: the step, the path it concerned and the reason, printed as one stderr line (exit 2)."""

    def __init__(self, step: str, path: str, reason: str) -> None:
        super().__init__(f"refused at {step}: {path}: {reason}")
        self.step = step
        self.path = path
        self.reason = reason


def errno_text(error: OSError) -> str:
    """`<strerror> (<ERRNO NAME>)`, the kernel's own words for a failed step."""
    code = errno.errorcode.get(error.errno, str(error.errno)) if error.errno is not None else "no errno"
    return f"{error.strerror or 'failed'} ({code})"


def read_all(fd: int, step: str, path: str) -> bytes:
    parts = []
    while True:
        try:
            chunk = os.read(fd, CHUNK)
        except OSError as error:
            raise Refusal(step, path, f"cannot read it: {errno_text(error)}") from None
        if not chunk:
            return b"".join(parts)
        parts.append(chunk)


def write_all(fd: int, data: bytes, step: str, path: str) -> None:
    view = memoryview(data)
    while view:
        try:
            written = os.write(fd, view)
        except OSError as error:
            raise Refusal(step, path, f"cannot write it: {errno_text(error)}") from None
        view = view[written:]


def close_quietly(fd: int) -> None:
    try:
        os.close(fd)
    except OSError:
        pass


def open_agent(agent_dir: str, uid: int) -> int:
    """The one descriptor every later step runs on: `agent/` itself, a directory of `uid` nobody else can write."""
    try:
        dfd = os.open(agent_dir, DIRECTORY_FLAGS)
    except OSError as error:
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            raise Refusal("open-agent", agent_dir, f"is a symbolic link or not a directory; {INSIDE}") from None
        raise Refusal("open-agent", agent_dir, f"cannot open it: {errno_text(error)}") from None
    try:
        info = os.fstat(dfd)
    except OSError as error:
        close_quietly(dfd)
        raise Refusal("fstat-agent", agent_dir, f"cannot read its identity: {errno_text(error)}") from None
    if not stat.S_ISDIR(info.st_mode):
        close_quietly(dfd)
        raise Refusal("fstat-agent", agent_dir, "is not a directory")
    if info.st_uid != uid:
        close_quietly(dfd)
        raise Refusal("fstat-agent", agent_dir, f"is owned by uid {info.st_uid}, not {uid}")
    if info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        close_quietly(dfd)
        mode = oct(stat.S_IMODE(info.st_mode))
        raise Refusal("fstat-agent", agent_dir, f"is writable by its group or by others (mode {mode}); {INSIDE}")
    return dfd


def open_config(dfd: int, agent_dir: str, uid: int) -> "tuple[int, tuple[int, int]] | None":
    """`config.yml` opened through the held descriptor with its identity (device, inode), None when the entry is
    absent (ENOENT alone); a link, an irregular entry or another uid's file refuses."""
    path = f"{agent_dir}/{CONFIG}"
    try:
        cfd = os.open(CONFIG, READ_FLAGS, dir_fd=dfd)
    except OSError as error:
        if error.errno == errno.ENOENT:
            return None
        if error.errno == errno.ELOOP:
            raise Refusal("open-config", path, f"is a symbolic link; {INSIDE}") from None
        raise Refusal("open-config", path, f"cannot open it: {errno_text(error)}") from None
    try:
        try:
            info = os.fstat(cfd)
        except OSError as error:
            raise Refusal("fstat-config", path, f"cannot read its identity: {errno_text(error)}") from None
        if not stat.S_ISREG(info.st_mode):
            raise Refusal("fstat-config", path, f"is not a regular file; {INSIDE}")
        if info.st_uid != uid:
            raise Refusal("fstat-config", path, f"is owned by uid {info.st_uid}, not {uid}")
    except Refusal:
        close_quietly(cfd)
        raise
    return cfd, (info.st_dev, info.st_ino)


def read_config(dfd: int, agent_dir: str, uid: int) -> "tuple[bytes | None, tuple[int, int] | None]":
    """The bytes of `config.yml` read through the held descriptor and the identity of the file they were read from,
    (None, None) when the entry is absent."""
    opened = open_config(dfd, agent_dir, uid)
    if opened is None:
        return None, None
    cfd, identity = opened
    try:
        return read_all(cfd, "read-config", f"{agent_dir}/{CONFIG}"), identity
    finally:
        close_quietly(cfd)


def identity_at(dfd: int, agent_dir: str, step: str, uid: int) -> "tuple[int, int]":
    """The identity of the entry `config.yml` names now, through one more open on the held descriptor; an absent
    entry refuses, since the name held the config a moment ago."""
    opened = open_config(dfd, agent_dir, uid)
    if opened is None:
        raise Refusal(
            step, f"{agent_dir}/{CONFIG}", "is absent after it held the rendered config (replaced during placement)"
        )
    cfd, identity = opened
    close_quietly(cfd)
    return identity


def settled(dfd: int, agent_dir: str, uid: int, rendered: bytes, identity: "tuple[int, int]", step: str) -> None:
    """The name `config.yml` holds the inode `identity` (the written temporary's after the rename, or the compared
    config's), read through the held directory descriptor; another inode there is read once and must hold the
    rendering and still stand at the name after that read (a concurrent launch of the same bytes); anything else
    refuses, so no replacement of the entry during a read is reported as placed or kept (an owner's rewrite in place
    is the residual the module docstring names)."""
    target = f"{agent_dir}/{CONFIG}"
    for attempt in (0, 1):
        if identity_at(dfd, agent_dir, step, uid) == identity:
            return
        if attempt:
            break
        current, identity = read_config(dfd, agent_dir, uid)
        if current != rendered:
            raise Refusal(
                step,
                target,
                "does not hold the rendered config after the rename (a writer inside the directory replaced it)",
            )
    raise Refusal(step, target, "config.yml replaced during placement (another inode at the name on every read)")


def create_temporary(dfd: int, agent_dir: str, uid: int) -> "tuple[str, int, tuple[int, int]]":
    """A fresh 0600 regular file of `uid` at a random name inside the held directory, created exclusively, with the
    identity (device, inode) of the descriptor."""
    name = TEMPORARY_PREFIX + secrets.token_hex(8)
    path = f"{agent_dir}/{name}"
    try:
        tfd = os.open(name, CREATE_FLAGS, 0o600, dir_fd=dfd)
    except OSError as error:
        if error.errno == errno.EEXIST:
            raise Refusal(
                "create-temporary", path, "an entry already stands at the temporary name; nothing was opened"
            ) from None
        raise Refusal(
            "create-temporary", path, f"cannot create a temporary file in {agent_dir}: {errno_text(error)}"
        ) from None
    try:
        try:
            info = os.fstat(tfd)
        except OSError as error:
            raise Refusal("fstat-temporary", path, f"cannot read its identity: {errno_text(error)}") from None
        if not stat.S_ISREG(info.st_mode) or info.st_uid != uid or info.st_nlink != 1:
            raise Refusal("fstat-temporary", path, "is not a fresh regular file of this user with one link")
        try:
            os.fchmod(tfd, 0o600)
        except OSError as error:
            raise Refusal("fchmod-temporary", path, f"cannot set its mode: {errno_text(error)}") from None
    except Refusal as refusal:
        close_quietly(tfd)
        raise unlink_temporary(dfd, name, path, refusal) from None
    return name, tfd, (info.st_dev, info.st_ino)


def unlink_temporary(dfd: int, name: str, path: str, refusal: Refusal) -> Refusal:
    """Remove the temporary through the held descriptor after a refusal; a removal that fails is named in the line."""
    try:
        os.unlink(name, dir_fd=dfd)
    except OSError as error:
        return Refusal(
            refusal.step, refusal.path, f"{refusal.reason}; the temporary {path} remains (unlink: {errno_text(error)})"
        )
    return refusal


def place(agent_dir: str, uid: int, rendered: bytes, dry_run: bool) -> str:
    """Place `rendered` as `config.yml` inside `agent_dir`, or raise Refusal; the decision word for stdout."""
    dfd = open_agent(agent_dir, uid)
    try:
        current, identity = read_config(dfd, agent_dir, uid)
        if current == rendered and identity is not None:
            settled(dfd, agent_dir, uid, rendered, identity, "verify-kept")
            return "kept"
        if dry_run:
            return "absent" if current is None else "differs"
        name, tfd, written = create_temporary(dfd, agent_dir, uid)
        path = f"{agent_dir}/{name}"
        target = f"{agent_dir}/{CONFIG}"
        try:
            write_all(tfd, rendered, "write-temporary", path)
            try:
                os.fsync(tfd)
            except OSError as error:
                raise Refusal("fsync-temporary", path, f"cannot flush it: {errno_text(error)}") from None
            try:
                os.rename(name, CONFIG, src_dir_fd=dfd, dst_dir_fd=dfd)
            except OSError as error:
                if error.errno in (errno.EISDIR, errno.ENOTEMPTY, errno.EEXIST, errno.ENOTDIR):
                    raise Refusal("rename", target, f"a directory stands at the destination; {INSIDE}") from None
                raise Refusal("rename", target, f"cannot install it: {errno_text(error)}") from None
        except Refusal as refusal:
            close_quietly(tfd)
            raise unlink_temporary(dfd, name, path, refusal) from None
        try:
            try:
                os.lseek(tfd, 0, os.SEEK_SET)
            except OSError as error:
                raise Refusal("verify-placed", target, f"cannot rewind the written file: {errno_text(error)}") from None
            if read_all(tfd, "verify-placed", target) != rendered:
                raise Refusal(
                    "verify-placed",
                    target,
                    "does not hold the rendered config after the rename (a writer inside the directory replaced it)",
                )
        finally:
            close_quietly(tfd)
        settled(dfd, agent_dir, uid, rendered, written, "verify-placed")
        return "placed" if current is None else "replaced"
    finally:
        close_quietly(dfd)


def main(argv: "list[str]", stdin) -> int:
    dry_run = False
    args = list(argv)
    if args and args[0] == "--dry-run":
        dry_run = True
        args = args[1:]
    absolute = len(args) == 2 and args[0].startswith("/")  # lint-comparisons: allow a shape test, no two paths compared
    if len(args) != 2 or args[0].startswith("-") or not absolute or not args[1].isdigit():
        print(USAGE, file=sys.stderr)
        return 1
    agent_dir, uid = args[0].rstrip("/") or "/", int(args[1])
    try:
        rendered = stdin.read()
    except OSError as error:
        print(f"{NAME}: cannot read the rendered config from stdin: {errno_text(error)}", file=sys.stderr)
        return 1
    try:
        decision = place(agent_dir, uid, rendered, dry_run)
    except Refusal as refusal:
        print(f"{NAME}: {refusal}", file=sys.stderr)
        return 2
    print(decision)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], sys.stdin.buffer))
