"""Shared probes of design-quality 5.14 item 7: one attack each in a temporary fixture, and the trusted parent."""

import contextlib
import functools
import hashlib
import json
import os
import pwd
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

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
            self._git(repo, "init", "-q")
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


class WorkerRoot:
    """An input, an output and a new output under a worker root. A read shows as the input's access time leaving 0; a
    filesystem where a read leaves it at 0 (measured on a scratch file) refuses the probe instead of passing vacuously."""

    def __init__(self, base):
        self.base, seat = base, base / "root" / ".claude" / "worktrees" / "probe-seat"
        seat.mkdir(parents=True)
        self.input, self.output, self.new_output = seat / "ledger.tsv", seat / "out.txt", seat / "new" / "out.txt"
        check = base / "atime-check"
        for path in (check, self.input, self.output):
            path.write_text(LEGIT)
            os.utime(path, ns=(0, BASELINE_NS))
        if check.read_text() and os.stat(check).st_atime_ns == 0:
            raise RuntimeError(f"a read leaves the access time at 0 under {base}, so reads are not observable here")
        self._inodes = {path: os.lstat(path).st_ino for path in (self.input, self.output)}

    def assert_untouched(self):
        """Nothing read the input, wrote, replaced or removed either file, or created the new output's directory. The
        content is compared too, since a write in place can keep the inode, the size and a coarse clock's mtime."""
        found = []
        for path, inode in self._inodes.items():
            if not os.path.lexists(path):
                found.append(f"removed {path}")
                continue
            st = os.lstat(path)
            found += [f"read {path}"] if path == self.input and st.st_atime_ns else []
            content = path.read_bytes() if st.st_ino == inode else b""  # the same file only, never through a new link
            os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=False)  # puts this read's access back
            if (st.st_ino, st.st_mtime_ns, content) != (inode, BASELINE_NS, LEGIT.encode()):
                found.append(f"wrote {path}")
        found += [f"created {self.new_output}"] if self.new_output.parent.exists() else []
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
    try:
        yield cls(base, *args)
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
