#!/usr/bin/env python3
"""`cat`, `ls` and `mkdir` as the fake codex's emulated sandbox runs them (tests/unit/test_pr_audit.py).

The fake `codex sandbox` runs the lever's real probe script with a directory of links to this file first on PATH. The
tool named by argv[0] acts on its last argument: a path under FAKE_SANDBOX_READ or FAKE_SANDBOX_WRITE (os.pathsep
lists) is read by the real tool, a new directory under FAKE_SANDBOX_WRITE is made by the real `mkdir`, and anything
else fails as macOS Seatbelt fails it, `<tool>: <path>: Operation not permitted` and exit 1. FAKE_SANDBOX_EXIT (for
example 42, 126 or 127) replaces that denial with a bare failure of that status and no denial text, the tool that
could not run; FAKE_SANDBOX_EXIT_ALL fails every call that way, the positive controls included.
"""

import os
import sys
from pathlib import Path

REAL = {"cat": "/bin/cat", "ls": "/bin/ls", "mkdir": "/bin/mkdir"}


def roots(name):
    return [os.path.realpath(p) for p in os.environ.get(name, "").split(os.pathsep) if p]


def under(path, allowed):
    path = Path(os.path.realpath(path))
    return any(path.is_relative_to(root) for root in allowed)


tool = os.path.basename(sys.argv[0])
target = sys.argv[-1]
every = os.environ.get("FAKE_SANDBOX_EXIT_ALL")
if every:
    sys.stderr.write(f"{tool}: could not run\n")
    sys.exit(int(every))
if tool == "mkdir":
    allowed = under(os.path.dirname(target.rstrip("/")) or "/", roots("FAKE_SANDBOX_WRITE"))
else:
    allowed = under(target, roots("FAKE_SANDBOX_READ") + roots("FAKE_SANDBOX_WRITE"))
if allowed:
    os.execv(REAL[tool], [REAL[tool], *sys.argv[1:]])
code = os.environ.get("FAKE_SANDBOX_EXIT")
if code:
    sys.stderr.write(f"{tool}: could not run\n")
    sys.exit(int(code))
sys.stderr.write(f"{tool}: {target}: Operation not permitted\n")
sys.exit(1)
