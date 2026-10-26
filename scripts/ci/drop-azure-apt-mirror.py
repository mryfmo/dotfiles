#!/usr/bin/env python3
"""Remove azure.archive.ubuntu.com from a GitHub-hosted Ubuntu runner's apt mirror list (regime-cutover U102).

actions/runner-images#14823 (open since 2026-09-30, ubuntu-24.04 and ubuntu-26.04): the runner image lists
azure.archive.ubuntu.com first in /etc/apt/apt-mirrors.txt and sets `Acquire::http::Timeout "15"` and
`Acquire::Retries "1"` (runner-images#14594). That timeout fires only when no data arrives for 15 s, so a node that
keeps sending archives slowly (61.5 kB/s for 20 minutes in the issue's run) never trips it, and apt never moves on to
the next entry; apt has no minimum-throughput setting. The issue's workaround is this script's: delete the Azure line,
so apt fetches from the next mirror in the list (archive.ubuntu.com).

Every workflow job that runs apt on a Ubuntu runner calls `/usr/bin/python3 -I -S scripts/ci/drop-azure-apt-mirror.py`
before its first apt use (tests/unit/test_apt_mirror.py checks the order); the system python3 is used, so no setup
step can change what runs. Usage: drop-azure-apt-mirror.py [list], the list defaulting to /etc/apt/apt-mirrors.txt.

The list is read with open(), filtered and counted in Python, written (directly when this user may, else through
`sudo -n tee`, its status checked and its time bounded) and read back and compared byte for byte. A list that would be
left with no mirror is refused. Exit 0: the Azure line is gone, was never there, or there is no list (not such a
runner). Exit 1, with a one-line reason: any read, write or comparison failure, or no mirror left.
"""

import os
import subprocess
import sys

DEFAULT = "/etc/apt/apt-mirrors.txt"
AZURE = b"azure.archive.ubuntu.com"
# sudo tee writes a few hundred bytes; a hung sudo (a password prompt cannot appear with -n) ends here.
WRITE_TIMEOUT = 60


class Refused(Exception):
    """A failure with its one-line reason."""


def read(path, when):
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as error:
        raise Refused(f"cannot read {path}{when}: {error.strerror or error}") from error


def write(path, data):
    if os.geteuid() == 0 or os.access(path, os.W_OK):
        try:
            with open(path, "wb") as handle:
                handle.write(data)
        except OSError as error:
            raise Refused(f"could not write {path}: {error.strerror or error}") from error
        return
    try:
        subprocess.run(
            ["sudo", "-n", "tee", path],
            input=data, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True, timeout=WRITE_TIMEOUT,
        )  # fmt: skip
    except subprocess.CalledProcessError as error:
        reason = error.stderr.decode(errors="replace").strip().splitlines()
        raise Refused(f"could not write {path}: sudo -n tee exited {error.returncode}: {' '.join(reason)}") from error
    except subprocess.TimeoutExpired as error:
        raise Refused(f"could not write {path}: sudo -n tee did not finish within {WRITE_TIMEOUT} s") from error
    except OSError as error:
        raise Refused(f"could not write {path}: cannot run sudo: {error.strerror or error}") from error


def show(label, data):
    print(f"{label}:\n{data.decode(errors='replace')}", end="" if data.endswith(b"\n") or not data else "\n")


def main(argv):
    path = argv[0] if argv else DEFAULT
    if not os.path.lexists(path):
        print(f"{path} is absent; no apt mirror list to change")
        return 0
    before = read(path, "")
    show(f"{path} before", before)
    lines = before.splitlines(keepends=True)
    kept = [line for line in lines if AZURE not in line]
    if len(kept) == len(lines):
        print(f"no azure.archive.ubuntu.com entry in {path}; nothing to change")
        return 0
    if not any(b"priority:" in line for line in kept):
        raise Refused(f"no apt mirror would be left in {path}; it is unchanged")
    after = b"".join(kept)
    write(path, after)
    if read(path, " back after the write") != after:
        raise Refused(f"{path} read back differs from what was written")
    show(f"{path} after", after)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Refused as refusal:
        print(f"drop-azure-apt-mirror: {refusal}", file=sys.stderr)
        sys.exit(1)
    except Exception as error:  # noqa: BLE001 - no silent path: any other failure is named and fails
        print(f"drop-azure-apt-mirror: unexpected {type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)
