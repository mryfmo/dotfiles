"""Exercise tests/unit/trusted_exec_contract.py: each probe fails for the intended reason on a noncompliant consumer stub
(so an inert attack or a no-op assertion fails the test), then passes a compliant one; fixtures are temporary."""

import errno
import functools
import hashlib
import os
import pwd
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
import trusted_exec_contract as tec

ROOT = Path(__file__).resolve().parents[2]
SHELL_NAMES = ("PWD", "SHLVL", "_")  # what bash exports to its own children (measured; a shell consumer declares them)
ARGS = ["a b", "", "$(echo injected)", "*", "two\nlines"]
ALLOWED_ENV = {"PATH": "/usr/bin:/bin", "HOME": "/h", "LANG": "C.UTF-8"}
SAFE_GIT = ["-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null"]
GIT_CLEAN = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
ATTACK_NAMES = {"GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM"}
ATTACK_NAMES |= {"GIT_CEILING_DIRECTORIES", "GIT_ALTERNATE_OBJECT_DIRECTORIES"}
REDIRECTED, HOOK = "attacker root .*; attacker content", "attacker hook ran"  # whole reasons: no part goes inert
ATTACKS = (("environment", f"{REDIRECTED}; {HOOK}"), ("local-worktree", REDIRECTED), ("local-include", HOOK))
# The tail of a scanner-open record: the UTC clock of the input's wake, then each control wake's offset from it.
WAKE_FORM = (
    r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ \(control woke [-+]\d+\.\d{3} s(, [-+]\d+\.\d{3} s)* from the input's wake\)$"
)


def run(argv, env, timeout=60, **kw):
    """A subprocess in a session of its own, with a deadline: one that hangs fails the test, and its whole process
    group (every descendant) is stopped first, TERM and then KILL, and waited for, so nothing is left running."""
    proc = subprocess.Popen(
        argv,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
        **kw,
    )
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        out, err = kill_group(proc)
        raise subprocess.TimeoutExpired(argv, timeout, output=out, stderr=err) from None
    return subprocess.CompletedProcess(argv, proc.returncode, out, err)


def kill_group(proc, grace=2):
    """Stop PROC's process group and return what PROC wrote: TERM, a GRACE-second wait, then KILL to the group in
    every case (a descendant may ignore TERM and have closed its output, so PROC finishing proves nothing about
    it), then wait. ESRCH (ProcessLookupError) means the group is already gone. macOS answers EPERM when the
    group is vanishing, its last members zombies being reaped (measured: 42 of 200 parallel runs, 1 of 40 serial,
    with ps then showing no member); that EPERM is accepted only after ps shows no live member of the group. Any
    other errno, or EPERM with a live member, is raised."""
    out = err = None
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass  # the whole group is gone already
    try:
        out, err = proc.communicate(timeout=grace)
    except subprocess.TimeoutExpired:
        pass  # PROC itself ignores TERM: KILL below
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass  # nothing of the group is left
    except PermissionError:
        if live_group_members(proc.pid):
            raise
    if out is None:
        out, err = proc.communicate()
    return out, err


def live_group_members(pgid):
    """The pids in process group PGID that are not zombies, read from ps (state Z is a zombie)."""
    listing = subprocess.run(
        ["/bin/ps", "-axo", "pid=,pgid=,stat="],
        env={"PATH": "/usr/bin:/bin"},
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    rows = (line.split() for line in listing.splitlines() if line.strip())
    return [int(pid) for pid, group, state in rows if int(group) == pgid and not state.startswith("Z")]


def naive_git(root, env):
    """Noncompliant: trusts the offered environment and repository configuration."""
    top = run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], env).stdout.decode().strip()
    run(["git", "-C", str(root), "status", "--porcelain"], env)
    return top, Path(top, "probe.txt").read_text()


def careful_git(root, env):
    """Compliant: no GIT_* from the caller, an explicit work tree and no repository-selected program."""
    env = {k: v for k, v in env.items() if not k.startswith("GIT_")} | GIT_CLEAN
    git = ["git", "-C", str(root), "--work-tree", str(root), *SAFE_GIT]
    run([*git, "status", "--porcelain"], env)
    top = run([*git, "rev-parse", "--show-toplevel"], env).stdout.decode().strip()
    return top, Path(root, "probe.txt").read_text()


def in_thread(target, timeout=30):
    """Run TARGET in another thread and return its result; a consumer that hangs (a blocking FIFO open nobody
    serves) fails the test after TIMEOUT instead of hanging the suite, and its exception is raised here."""
    import threading

    outcome = {}

    def body():
        try:
            outcome["value"] = target()
        except BaseException as error:  # noqa: BLE001 - handed to the test thread
            outcome["error"] = error

    thread = threading.Thread(target=body, name="consumer", daemon=True)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise AssertionError(f"consumer still running after {timeout}s: it hung")
    if "error" in outcome:
        raise outcome["error"]
    return outcome.get("value")


def read_relative(path):
    """Read PATH by its bare name from its own directory (the working directory is put back)."""
    here = os.getcwd()
    os.chdir(Path(path).parent)
    try:
        return Path(Path(path).name).read_bytes()
    finally:
        os.chdir(here)


def swap_and_restore(probe, swap_in):
    """Move the input FIFO aside, put SWAP_IN's file in its place until the probe's identity check looked twice,
    put it back."""
    aside = probe.base / "aside"
    os.rename(probe.input, aside)
    swap_in(probe.input)
    seen = probe.checks
    while probe.checks < seen + 2:
        time.sleep(0.001)
    os.unlink(probe.input)
    os.rename(aside, probe.input)


def naive_io(probe):
    """Noncompliant: reads its input and writes its outputs wherever they are."""
    data = Path(probe.input).read_text()
    Path(probe.output).write_text(data)
    Path(probe.new_output).parent.mkdir(parents=True, exist_ok=True)
    Path(probe.new_output).write_text(data)


def guarded_io(probe):
    """Compliant: every trusted path is resolved first and refused under a worker root."""
    for path in (probe.input, probe.output, probe.new_output):
        if "/.claude/worktrees/" in os.path.realpath(path) + "/":
            raise PermissionError(f"{path}: under a worker root")
    naive_io(probe)


def by_path(path, sha, between):
    """Noncompliant: checks the file, then opens it again by name."""
    if hashlib.sha256(Path(path).read_bytes()).hexdigest() != sha:
        raise ValueError("check failed")
    between()
    return Path(path).read_bytes()


def by_snapshot(path, sha, between):
    """Compliant: checks and uses one snapshot, read through one descriptor that refuses a link."""
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), "rb") as handle:
        data = handle.read()
    if hashlib.sha256(data).hexdigest() != sha:
        raise ValueError("check failed")
    between()
    return data


class TrustedExecContractTest(tec.TrustedExecContractMixin, unittest.TestCase):
    def runner_fixture(self):
        """A root whose script records its argv and environment; only the passwd response and the root are substituted."""
        base = Path(self.enter(tempfile.TemporaryDirectory)).resolve()
        root, home, out = base / "root", base / "home", base / "out"
        for d in (root / "scripts", home, out):
            d.mkdir(parents=True)
        script = root / "scripts" / "observe.sh"
        script.write_text(f'printf "%s\\0" "$0" "$@" > "{out}/argv"\n/usr/bin/env -0 > "{out}/env"\n')
        linux = f"me:*:{os.getuid()}:0::{home}:/bin/sh\n"
        response = f"NFSHomeDirectory: {home}\n" if sys.platform == "darwin" else linux
        self.enter(
            mock.patch.object, tec.pwd, "getpwuid", return_value=pwd.struct_passwd(("me", "*", 0, 0, "", str(home), ""))
        )
        self.enter(mock.patch.object, tec, "_directory_service", return_value=response)
        self.enter(mock.patch.object, tec, "repository_root", return_value=root)

        def check(args):
            argv = [a.decode() for a in (out / "argv").read_bytes().split(b"\0")[:-1]]
            env = tec.parse_env((out / "env").read_bytes())
            for f in out.iterdir():
                f.unlink()
            if argv != [str(script), *args]:
                raise AssertionError(f"argv: {argv!r}")
            tec.assert_sanitized_env(env, SHELL_NAMES)
            if env["HOME"] != str(home):
                raise AssertionError(f"HOME is {env['HOME']!r}")

        return SimpleNamespace(base=base, root=root, home=home, out=out, script=script, check=check)

    # The six sensitivity cases: red on a noncompliant stub, then green on a compliant one.

    def case_shim_on_path(self):
        probe = self.shim_probe(dict(os.environ))
        run(["git", "status", "a b", ""], probe.env)
        with self.assertRaisesRegex(AssertionError, "shim ran: git") as red:
            probe.assert_none_ran()
        clean = self.shim_probe(dict(os.environ))
        run(["/bin/echo", "ok"], clean.env)
        clean.assert_none_ran()
        return str(red.exception)

    def case_hostile_git(self):
        probe, reasons = self.hostile_git_probe(), []
        for kind, reason in ATTACKS:
            with probe.attack(kind) as env, self.assertRaisesRegex(AssertionError, reason) as red:
                probe.assert_unaffected(*naive_git(probe.legit, env))
            reasons.append(f"{kind}: {red.exception}")
            with probe.attack(kind) as env:
                probe.assert_unaffected(*careful_git(probe.legit, env))
        return "; ".join(reasons)

    def case_worker_root(self):
        probe = self.worker_root_probe()
        probe.consume(lambda: naive_io(probe))
        with self.assertRaisesRegex(AssertionError, "worker root: read .*; wrote .*; created ") as red:
            probe.assert_untouched()
        clean = self.worker_root_probe()
        with self.assertRaises(PermissionError):
            clean.consume(lambda: guarded_io(clean))
        for _ in range(2):  # twice: the probe's own content read must not count as a read
            clean.assert_untouched()
        return str(red.exception)

    def case_swapped_file(self):
        probe = self.swapped_file_probe()
        data = by_path(probe.path, probe.expected_sha, probe.swap)
        with self.assertRaisesRegex(AssertionError, "attacker content consumed") as red:
            probe.assert_not_consumed(data)
        clean = self.swapped_file_probe()
        clean.assert_not_consumed(by_snapshot(clean.path, clean.expected_sha, clean.swap))
        return str(red.exception)

    def case_sanitized_environment(self):
        leaky = run(["/usr/bin/env", "-0"], os.environ | ALLOWED_ENV | {"LEAK": "1"})
        with self.assertRaisesRegex(AssertionError, "undeclared: .*'LEAK'") as red:
            tec.assert_sanitized_env(tec.parse_env(leaky.stdout))
        clean = run(["/usr/bin/env", "-0"], ALLOWED_ENV)
        tec.assert_sanitized_env(tec.parse_env(clean.stdout))
        return str(red.exception)

    def case_trusted_parent(self):
        fx = self.runner_fixture()
        inherited = os.environ | {"HOME": str(fx.home), "BASH_ENV": ""}  # the caller's names; never the real home
        run(["/bin/bash", str(fx.script), *ARGS], inherited, cwd=fx.base)
        with self.assertRaisesRegex(AssertionError, "undeclared") as red:
            fx.check(ARGS)
        with mock.patch.object(tec.subprocess, "run", wraps=subprocess.run) as spy:  # still runs; argv and env observed
            result = tec.run_under_trusted_parent(fx.script, *ARGS)
        self.assertEqual(0, result.returncode, result.stderr)
        fx.check(ARGS)
        argv = ["/usr/bin/env", "-i", "PATH=/usr/bin:/bin", f"HOME={fx.home}", "LANG=C.UTF-8"]
        argv += ["/bin/bash", "--noprofile", "--norc", "-p", str(fx.script), *ARGS]
        self.assertEqual((argv, {}), (spy.call_args.args[0], spy.call_args.kwargs["env"]))
        return str(red.exception)

    CASES = ("shim_on_path", "hostile_git", "worker_root", "swapped_file", "sanitized_environment", "trusted_parent")

    def test_each_probe_detects_condition(self):
        for name in self.CASES:
            with self.subTest(name):
                self.assertTrue(getattr(self, f"case_{name}")())

    def test_shim_probe(self):
        self.case_shim_on_path()
        probe = self.shim_probe({"PATH": "/usr/bin:/bin"})
        self.assertEqual(f"{probe.bin}{os.pathsep}/usr/bin:/bin", probe.env["PATH"])
        for name in tec.SHIMS:
            self.assertEqual(97, run([name, "--flag", "a b"], probe.env).returncode)
        expected = [{"name": n, "argv": [str(probe.bin / n), "--flag", "a b"]} for n in tec.SHIMS]
        self.assertEqual(expected, probe.records())

    def test_hostile_git_probe(self):
        listing = ["git", "-C", str(ROOT), "config", "--list", "--show-origin"]
        config = lambda: run(listing, {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent"}).stdout
        before = config()
        self.case_hostile_git()
        probe = self.hostile_git_probe()
        with self.assertRaises(RuntimeError), probe.attack("local-worktree"):
            raise RuntimeError("deliberate")
        self.assertNotIn("worktree", (probe.legit / ".git" / "config").read_text())
        with probe.attack("environment") as env:
            self.assertEqual(ATTACK_NAMES, {k for k in env if k.startswith("GIT_")})
            oid = run(["git", "-C", str(probe.attacker), "rev-parse", ":probe.txt"], env).stdout.decode().strip()
            legit, sub, plain = probe.legit, probe.legit / "sub", {"PATH": "/usr/bin:/bin", "HOME": str(probe.base)}
            sub.mkdir()
            has = lambda text: lambda r: text in r.stdout
            for name, args, where, effect in (  # each hostile name alone changes what git does in the legitimate repo
                ("GIT_DIR", ["rev-parse", "--absolute-git-dir"], legit, has(b"attacker")),
                ("GIT_WORK_TREE", ["rev-parse", "--show-toplevel"], legit, has(b"attacker")),
                ("GIT_CONFIG_GLOBAL", ["config", "--global", "core.fsmonitor"], legit, has(b"hook")),
                ("GIT_CONFIG_SYSTEM", ["config", "--system", "core.fsmonitor"], legit, has(b"hook")),
                ("GIT_CEILING_DIRECTORIES", ["rev-parse", "--show-toplevel"], sub, lambda r: r.returncode),
                ("GIT_ALTERNATE_OBJECT_DIRECTORIES", ["cat-file", "-e", oid], legit, lambda r: not r.returncode),
            ):
                alone, without = (run(["git", "-C", str(where), *args], e) for e in (plain | {name: env[name]}, plain))
                self.assertTrue(effect(alone) and not effect(without), name)
        with probe.attack("local-worktree") as env:  # the local attack alone, in an environment without GIT_*
            self.assertFalse([k for k in env if k.startswith("GIT_")])
            self.assertIn("worktree", (probe.legit / ".git" / "config").read_text())
        self.assertEqual(before, config())

    def test_worker_root_probe(self):
        self.case_worker_root()
        shell = lambda line: lambda p: run(["/bin/sh", "-c", line, str(p.input)], ALLOWED_ENV)  # a subprocess consumer
        for name, act, reason in (
            ("read", lambda p: Path(p.input).read_text(), "read "),
            ("read with os.open", lambda p: os.close(os.open(p.input, os.O_RDONLY)), "read "),
            ("read by a subprocess", shell('cat "$0" > /dev/null'), "read "),
            ("read by a relative path after chdir", lambda p: read_relative(p.input), "read "),
            ("read by another thread", lambda p: in_thread(lambda: Path(p.input).read_bytes()), "read "),
            (
                "read through a symlink",
                lambda p: (p.base / "alias").symlink_to(p.input) or (p.base / "alias").read_text(),
                "read ",
            ),
            (
                "read through a hard link",
                lambda p: os.link(p.input, p.base / "hard") or (p.base / "hard").read_text(),
                "read ",
            ),
            ("wrote", lambda p: Path(p.output).write_text("x"), "wrote "),
            ("created", lambda p: (Path(p.new_output).parent.mkdir(), Path(p.new_output).write_text("x")), "created "),
            ("appended", lambda p: run(["/bin/sh", "-c", 'echo x >> "$0"', str(p.output)], ALLOWED_ENV), "wrote "),
            ("replaced", shell('echo x > "$0.t"; mv "$0.t" "$0"'), "wrote "),
            ("removed", lambda p: os.unlink(p.input), "removed "),
        ):
            with self.subTest(name):
                probe = self.worker_root_probe()
                self.assertIn("/.claude/worktrees/", str(probe.input))
                self.assertFalse(Path(probe.new_output).exists())
                probe.consume(functools.partial(act, probe))
                with self.assertRaisesRegex(AssertionError, reason):
                    probe.assert_untouched()

    def test_swapped_file_probe(self):
        self.case_swapped_file()
        probe = self.swapped_file_probe()
        with self.assertRaisesRegex(AssertionError, "never swapped"):  # a consumer that skipped the barrier
            probe.assert_not_consumed(Path(probe.path).read_bytes())
        with self.subTest("case-alias"):
            alias = self.swapped_file_probe()
            if alias.alias is None:
                self.skipTest(f"case-alias unsupported: {alias.alias_reason}")
            self.assertTrue(os.path.samefile(alias.alias, alias.path))
            data = by_path(alias.path, alias.expected_sha, lambda: alias.swap(via_alias=True))
            with self.assertRaisesRegex(AssertionError, "attacker content consumed"):
                alias.assert_not_consumed(data)
            clean = self.swapped_file_probe()
            clean.assert_not_consumed(by_snapshot(clean.path, clean.expected_sha, lambda: clean.swap(via_alias=True)))

    def test_sanitized_environment_probe(self):
        self.case_sanitized_environment()
        tec.assert_sanitized_env(ALLOWED_ENV | {"SHLVL": "1"}, declared=("SHLVL",))
        for observed, declared, reason in (
            ({"PATH": "/usr/bin:/bin", "HOME": "/h"}, (), r"missing: \['LANG'\]"),
            (ALLOWED_ENV | {"PATH": "/usr/local/bin:/usr/bin:/bin"}, (), "PATH is"),
            (ALLOWED_ENV | {"SHLVL": "1"}, (), r"undeclared: \['SHLVL'\]"),
            (ALLOWED_ENV, ("SHLVL",), r"missing: \['SHLVL'\]"),
        ):
            with self.subTest(reason), self.assertRaisesRegex(AssertionError, reason):
                tec.assert_sanitized_env(observed, declared)

    def test_trusted_parent_probe(self):
        with mock.patch.dict(os.environ, {"GIT_DIR": "/nonexistent", "GIT_WORK_TREE": "/nonexistent"}):
            self.assertEqual(ROOT, tec.repository_root())  # the real discovery, before any fixture substitutes it
        self.case_trusted_parent()
        fx = self.runner_fixture()
        env = {"PATH": "/usr/bin:/bin", "HOME": str(fx.home), "LANG": "C.UTF-8"}
        run(["/bin/bash", "-c", f"/bin/bash {fx.script} " + " ".join(ARGS[:2])], env, cwd=fx.base)  # word-split argv
        with self.assertRaisesRegex(AssertionError, "argv"):
            fx.check(ARGS[:2])
        (outside := fx.base / "outside").mkdir()
        (outside / "x.sh").write_text(f'echo ran > "{fx.out}/marker"\n')
        (fx.root.parent / "root-evil").mkdir()
        (fx.root.parent / "root-evil" / "x.sh").write_text(f'echo ran > "{fx.out}/marker"\n')
        (fx.root / "link.sh").symlink_to(outside / "x.sh")
        for name, script, reason in (
            ("relative", "scripts/observe.sh", "not an absolute path"),
            ("traversal", f"{fx.root}/../outside/x.sh", "outside"),
            ("sibling-prefix", f"{fx.root}-evil/x.sh", "outside"),
            ("symlink escape", f"{fx.root}/link.sh", "outside"),
            ("directory", f"{fx.root}/scripts", "not a regular file"),
            ("missing", f"{fx.root}/scripts/none.sh", "not a regular file"),
        ):
            with self.subTest(name), self.assertRaisesRegex(tec.TrustedExecRefused, reason):
                tec.run_under_trusted_parent(script)
            self.assertFalse((fx.out / "marker").exists())

    def assert_stat_ran(self, result, path):
        """/usr/bin/stat exited 0 and described PATH: the metadata look really happened."""
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn(os.fsencode(path.name), result.stdout)

    def test_metadata_reads_and_other_files_are_not_reads_of_the_input(self):
        # U92 root cause: the probe saw a read as the input's access time leaving 0, and any process that opens a fresh
        # regular file sets it as well (on the macOS host a scanner read new temporary files within a second), so the
        # compliant consumer failed about once in 64 runs. The input is now a FIFO: only an open for reading counts.
        probe = self.worker_root_probe()
        self.assertTrue(stat.S_ISFIFO(os.lstat(probe.input).st_mode))

        def looks_only():
            os.stat(probe.input), os.path.realpath(probe.input), os.access(probe.input, os.R_OK)
            os.close(os.open(probe.base / "elsewhere", os.O_WRONLY | os.O_CREAT))
            Path(probe.base / "elsewhere").read_text()
            return run(["/usr/bin/stat", str(probe.input)], ALLOWED_ENV)  # another process looking, not opening

        self.assert_stat_ran(probe.consume(looks_only), probe.input)
        # Injected: a stat that fails, or exits 0 without describing the input, fails that check.
        for line, why in (('/usr/bin/stat "$0"; exit 4', "exit"), (': "$0"', "output")):
            with self.subTest(injected=why):
                result = probe.consume(functools.partial(run, ["/bin/sh", "-c", line, str(probe.input)], ALLOWED_ENV))
                with self.assertRaises(AssertionError):
                    self.assert_stat_ran(result, probe.input)
        with self.assertRaises(PermissionError):
            probe.consume(lambda: guarded_io(probe))
        probe.assert_untouched()
        probe.assert_untouched()

    def assert_eof(self, result):
        """A reader of the sentinel exits 0 and reads nothing: EOF, never content."""
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stdout)

    def test_a_blocking_reader_never_hangs_and_gets_eof(self):
        probe = self.worker_root_probe()
        self.assert_eof(probe.consume(lambda: run(["/bin/cat", str(probe.input)], ALLOWED_ENV)))
        with self.assertRaisesRegex(AssertionError, "worker root: read "):
            probe.assert_untouched()
        probe = self.worker_root_probe()
        self.assertEqual(b"", probe.consume(lambda: in_thread(lambda: Path(probe.input).read_bytes())))
        with self.assertRaisesRegex(AssertionError, "worker root: read "):
            probe.assert_untouched()
        # Injected: a reader that gets EOF and still exits non-zero, or exits 0 with output, fails the EOF check.
        for line, why in (('cat "$0"; exit 7', "exit"), ('cat "$0"; echo leaked', "output")):
            with self.subTest(injected=why):
                probe = self.worker_root_probe()
                result = probe.consume(functools.partial(run, ["/bin/sh", "-c", line, str(probe.input)], ALLOWED_ENV))
                with self.assertRaises(AssertionError):
                    self.assert_eof(result)

    def test_a_recorded_read_names_its_holder(self):
        # U166: two 2026-11-04 runs on the ubuntu-24.04 server cell recorded a read no step of the test made, and the
        # record could not say who. It now names the holders /proc shows at the scan: a subprocess reader by its own
        # pid, an in-process thread by ours; a host without /proc says so. The host's form is asserted, nothing skipped.
        import re

        probe = self.worker_root_probe()
        self.assert_eof(probe.consume(lambda: run(["/bin/cat", str(probe.input)], ALLOWED_ENV)))
        with self.assertRaises(AssertionError) as by_cat:
            probe.assert_untouched()
        probe = self.worker_root_probe()
        self.assertEqual(b"", probe.consume(lambda: in_thread(lambda: Path(probe.input).read_bytes())))
        with self.assertRaises(AssertionError) as by_thread:
            probe.assert_untouched()
        if os.path.isdir("/proc"):
            cat = re.search(r"opened for reading by pid (\d+) \(cat, ppid \d+: /bin/cat ", str(by_cat.exception))
            self.assertIsNotNone(cat, str(by_cat.exception))
            self.assertNotEqual(os.getpid(), int(cat.group(1)))
            self.assertRegex(str(by_thread.exception), rf"opened for reading by pid {os.getpid()} \(")
        else:
            self.assertRegex(str(by_cat.exception), r"opened for reading reader not identified \(no /proc\)$")
            self.assertRegex(str(by_thread.exception), r"opened for reading reader not identified \(no /proc\)$")

    def holder_scan(self, probe):
        """probe._holders with a writer descriptor obtained the way the input's sentinel holds one: our own reader of
        the sentinel is what makes the write-open succeed, and both descriptors are closed again before the record is
        returned."""
        reader = os.open(probe.input, os.O_RDONLY | os.O_NONBLOCK)
        try:
            writer = probe._open_writer()
            self.assertIsNotNone(writer, f"a reader of {probe.input} did not make the write-open succeed")
            try:
                return probe._holders(writer)
            finally:
                os.close(writer)
        finally:
            os.close(reader)

    def test_the_holder_scan_names_a_holder_from_the_descriptor_table(self):
        # The scan reads PROC_ROOT, so a scratch tree of the same shape proves the record on every host: a symlink
        # stats to the sentinel's own (st_dev, st_ino) whether or not this one has a real /proc.
        probe = self.worker_root_probe()
        probe.consume(lambda: None)  # opens nothing, so no write-open of the sentinel succeeds by itself
        self.assertEqual([], probe.reads)
        proc = probe.base / "proc"
        probe.PROC_ROOT = str(proc)
        holder = proc / "4242"
        (holder / "fd").mkdir(parents=True)
        os.symlink(probe.input, holder / "fd" / "7")
        (holder / "comm").write_text("cat\n")
        (holder / "status").write_text("Name:\tcat\nPPid:\t77\n")
        (holder / "cmdline").write_bytes(b"/bin/cat\0" + os.fsencode(probe.input) + b"\0")
        self.assertEqual(f"by pid 4242 (cat, ppid 77: /bin/cat {probe.input} )", self.holder_scan(probe))
        blocked = proc / "4343" / "fd"
        blocked.mkdir(parents=True)
        blocked.chmod(0o000)
        self.addCleanup(blocked.chmod, 0o700)
        with self.assertRaises(PermissionError):  # root could list it, and the count below would be 0 instead
            os.listdir(blocked)
        shutil.rmtree(holder)
        self.assertEqual("by no process whose descriptors this user can read (1 unreadable)", self.holder_scan(probe))

    def unnamed_record(self):
        """What _holders says when no holder is named on this host: the no-holder count on a host with /proc, the
        no-tree form elsewhere; as a regex."""
        if os.path.isdir("/proc"):
            return r"by no process whose descriptors this user can read \(\d+ unreadable\)"
        return r"reader not identified \(no /proc\)"

    def hold_the_scan_until(self, probe, event):
        """Patch os.listdir for the test so the scan's listings of the proc root wait for EVENT (set by a reader after
        its close): the holder is gone when the scan looks, on any scheduler, as it was on the runner."""
        listdir = os.listdir

        def listing(path, *args, **kwargs):
            if path == probe.PROC_ROOT:
                event.wait(30)
            return listdir(path, *args, **kwargs)

        self.enter(mock.patch.object, tec.os, "listdir", listing)

    def test_an_input_open_with_no_holder_and_the_control_silent_is_the_consumers_read(self):
        """U625 round 3, the CI case: at 21e0da60 (run 44599355380, job 135826206740, the ubuntu-24.04 client leg)
        test_worker_root_probe [read with os.open] failed because the test's own same-user reader opened the sentinel
        and closed again before the scan listed it; the scan named nobody with 177 unreadable tables, the round-1 rule
        sent the open to `unattributed`, and the read the test expects went unrecorded. The reader here is that one, a
        thread that opens and closes at once, and the scan's listing of the proc root is held until it has closed, so
        no holder is named on Linux either (a host without /proc names nobody anyway). The control FIFO is untouched,
        so the open is the consumer's read, recorded with `(control silent)` before the pre-U625 record, and
        assert_untouched fails naming it; nothing is a scanner open and nothing is printed."""
        import contextlib
        import io
        import re
        import threading

        probe = self.worker_root_probe()
        closed = threading.Event()
        self.hold_the_scan_until(probe, closed)

        def open_and_close():
            os.close(os.open(probe.input, os.O_RDONLY))
            closed.set()

        with contextlib.redirect_stderr(io.StringIO()) as printed:
            probe.consume(lambda: in_thread(open_and_close))
        self.assertTrue(closed.is_set(), "the reader never closed")
        with self.assertRaisesRegex(AssertionError, "worker root: read ") as silent:
            probe.assert_untouched()
        form = re.escape(f"{probe.input} (control silent) opened for reading ") + self.unnamed_record() + "$"
        self.assertRegex(str(silent.exception), form)
        self.assertGreaterEqual(len(probe.reads), 1)  # the re-arm returns at once while the reader holds the input
        for entry in probe.reads:
            self.assertRegex(entry, form)
        self.assertEqual(([], []), (probe.scanner_opens, probe.errors))
        self.assertEqual("", printed.getvalue())

    def test_an_input_open_with_no_holder_beside_a_control_open_is_a_scanner_open(self):
        """U625 round 3: a directory scanner opens what it finds, so one that opened the sentinel opens the control
        FIFO beside it too. The scanner here is a thread that opens and closes each FIFO at once, the control first and
        then, in a second probe, the input first (a listing's order is the filesystem's), with the scan's listing held
        until the input's reader has closed as in the test above, so no holder is named on any host. Each input open
        lies beside a control open inside CONTROL_WINDOW_S: it is a scanner open, recorded naming both FIFOs with the
        unreadable count, the time and each control wake's offset, printed as `worker root: scanner open: ...`, and
        assert_untouched passes; nothing is a read."""
        import contextlib
        import io
        import re
        import threading

        for name, control_first in (("control first", True), ("input first", False)):
            with self.subTest(name):
                probe = self.worker_root_probe()
                input_closed = threading.Event()
                self.hold_the_scan_until(probe, input_closed)
                order = (probe.control, probe.input) if control_first else (probe.input, probe.control)

                def scanner(order=order, closed=input_closed, input=probe.input):
                    for path in order:
                        os.close(os.open(path, os.O_RDONLY))
                        if path == input:
                            closed.set()

                with contextlib.redirect_stderr(io.StringIO()) as printed:
                    probe.consume(lambda: in_thread(scanner))
                self.assertTrue(input_closed.is_set(), "the scanner never closed the input")
                probe.assert_untouched()
                self.assertEqual(([], []), (probe.reads, probe.errors))
                self.assertGreaterEqual(len(probe.scanner_opens), 1, printed.getvalue())
                form = re.escape(f"{probe.input} opened for reading ") + self.unnamed_record()
                form += re.escape(f", and {probe.control} opened for reading inside its window at ")
                form += WAKE_FORM
                for entry in probe.scanner_opens:
                    self.assertRegex(entry, form)
                    self.assertIn(f"worker root: scanner open: {entry}\n", printed.getvalue())

    def test_a_named_holder_fails_naming_its_pid_even_when_the_control_was_opened_too(self):
        """U625 round 3: a lever that happens to read beside a scanner is still a read. The reader is a thread of this
        process that reads the sentinel to EOF, so it holds its descriptor through the holder scan and is named by its
        pid on a host with /proc, while another thread opens the control at the same time. A host without /proc names
        nobody, so there the scan is pointed at a scratch tree of /proc's shape that names pid 4242 (the tree of
        test_the_holder_scan_names_a_holder_from_the_descriptor_table) while both readers stay real. The named pid is
        asserted in each case; the control open was seen, and nothing is a scanner open."""
        import contextlib
        import io
        import re
        import threading

        probe = self.worker_root_probe()
        if os.path.isdir("/proc"):
            named = rf"opened for reading by pid {os.getpid()} \("
        else:
            proc = probe.base / "proc"
            probe.PROC_ROOT = str(proc)
            holder = proc / "4242"
            (holder / "fd").mkdir(parents=True)
            os.symlink(probe.input, holder / "fd" / "7")
            (holder / "comm").write_text("cat\n")
            (holder / "status").write_text("Name:\tcat\nPPid:\t77\n")
            (holder / "cmdline").write_bytes(b"/bin/cat\0" + os.fsencode(probe.input) + b"\0")
            named = r"opened for reading by pid 4242 \(cat, ppid 77: /bin/cat "

        def lever_beside_a_scanner():
            control = threading.Thread(target=lambda: os.close(os.open(probe.control, os.O_RDONLY)), daemon=True)
            control.start()
            data = Path(probe.input).read_bytes()
            control.join(30)
            return data, control.is_alive()

        with contextlib.redirect_stderr(io.StringIO()) as printed:
            self.assertEqual((b"", False), probe.consume(lambda: in_thread(lever_beside_a_scanner)))
        with self.assertRaisesRegex(AssertionError, "worker root: read ") as by_pid:
            probe.assert_untouched()
        self.assertRegex(str(by_pid.exception), re.escape(str(probe.input)) + " " + named)
        self.assertGreaterEqual(len(probe._control_wakes), 1, "the control's reader was not seen")
        self.assertEqual(([], []), (probe.scanner_opens, probe.errors))
        self.assertEqual("", printed.getvalue())

    def scratch_proc_tree(self, entries, unreadable=1):
        """A tree of /proc's shape under a scratch directory for the holder scan to walk: ENTRIES pids, each with a
        descriptor table of one descriptor on another file (listed and stat'ed, never a match), and UNREADABLE
        tables of mode 0000 (another user's, as on a runner). The scan names nobody there, so it rescans for
        HOLDER_WAIT_S, and each pass lists ENTRIES tables: the time a sample between two passes was blind for."""
        proc = self.scratch("trusted-exec-proc-")
        for pid in range(1000, 1000 + entries):
            table = proc / str(pid) / "fd"
            table.mkdir(parents=True)
            os.symlink(os.devnull, table / "3")
        for pid in range(900, 900 + unreadable):
            blocked = proc / str(pid) / "fd"
            blocked.mkdir(parents=True)
            blocked.chmod(0o000)
            self.addCleanup(blocked.chmod, 0o700)
            with self.assertRaises(PermissionError):  # root could list it, and the count below would be 0 instead
                os.listdir(blocked)
        return proc

    def test_a_control_open_of_under_a_millisecond_during_the_holder_scan_is_a_scanner_open(self):
        """U625 round 5 (verdict of b26cbb87, P1 f2 s5): the round-4 probe sampled the control between two passes of
        the holder scan, and one pass over 150 or more /proc entries takes longer than a scanner needs to open and
        close the control, so a control open inside a pass fell between two samples and the input's open became the
        consumer's read with `(control silent)`. The scanner here is a thread: it opens the input (the latch is a
        writer, so the open returns at once and the scan starts), waits until the scan has listed the tree and then
        a random part of the scan's HOLDER_WAIT_S more, opens the control with O_NONBLOCK and closes it at once
        (tens of microseconds; a blocking open would have waited for the round-4 probe's next sample and been seen
        by it), then closes the input. The scan walks a scratch tree of 200 descriptor tables, slow enough that a
        sample between two passes is blind for the whole flicker. Twenty repetitions, each a probe of its own: every
        one is a scanner open, printed, and assert_untouched passes; none is a read. Red on the round-4 probe."""
        import contextlib
        import io
        import random
        import re
        import threading

        proc, moments = self.scratch_proc_tree(200), random.Random()
        record = r"by no process whose descriptors this user can read \(1 unreadable\)"
        for repetition in range(20):
            delay = moments.uniform(0.0, 0.1)
            with self.subTest(repetition=repetition, delay=round(delay, 4)):
                probe = self.worker_root_probe()
                probe.PROC_ROOT = str(proc)
                inside, listdir = threading.Event(), os.listdir

                def listing(path, *args, root=str(proc), inside=inside, real=listdir, **kwargs):
                    if path == root:
                        inside.set()
                    return real(path, *args, **kwargs)

                def scanner(probe=probe, inside=inside, delay=delay):
                    fd = os.open(probe.input, os.O_RDONLY)  # returns at once: the latch is a writer; the scan starts
                    try:
                        if not inside.wait(30):
                            raise AssertionError("the holder scan never listed the tree")
                        time.sleep(delay)
                        started = time.perf_counter()
                        os.close(os.open(probe.control, os.O_RDONLY | os.O_NONBLOCK))  # the flicker
                        return time.perf_counter() - started
                    finally:
                        os.close(fd)

                patched = mock.patch.object(tec.os, "listdir", listing)
                with patched, contextlib.redirect_stderr(io.StringIO()) as printed:
                    held = probe.consume(lambda: in_thread(scanner))
                try:
                    probe.assert_untouched()
                except AssertionError as failed:
                    self.fail(f"{failed} (the control was held {held * 1e6:.0f} us)")
                self.assertEqual(([], []), (probe.reads, probe.errors))
                self.assertGreaterEqual(len(probe.scanner_opens), 1, printed.getvalue())
                form = re.escape(f"{probe.input} opened for reading ") + record
                form += re.escape(f", and {probe.control} opened for reading inside its window at ") + WAKE_FORM
                for entry in probe.scanner_opens:
                    self.assertRegex(entry, form)
                    self.assertIn(f"worker root: scanner open: {entry}\n", printed.getvalue())

    def test_an_input_open_of_under_a_millisecond_with_the_control_untouched_is_a_read_every_time(self):
        """U625 round 5, the CI case kept strict (21e0da60, run 44599355380: the test's own reader opened the input and
        closed it before any look of the probe landed). A lever-like reader, a thread that opens the input for
        reading and closes it at once (the open returns at once, the latch being a writer; tens of microseconds in
        all) and never touches the control. The input's sentinel wakes for it every time: twenty repetitions, each
        a probe of its own, each a read, with `(control silent)` or the holder named (on Linux the scan can still
        find the thread's descriptor), and assert_untouched fails on it; nothing is a scanner open, nothing is
        printed."""
        import contextlib
        import io
        import re

        for repetition in range(20):
            with self.subTest(repetition=repetition):
                probe = self.worker_root_probe()

                def lever(probe=probe):
                    started = time.perf_counter()
                    os.close(os.open(probe.input, os.O_RDONLY))
                    return time.perf_counter() - started

                with contextlib.redirect_stderr(io.StringIO()) as printed:
                    held = probe.consume(lambda: in_thread(lever))
                with self.assertRaisesRegex(AssertionError, "worker root: read ") as read:
                    probe.assert_untouched()
                self.assertIn(f"{probe.input} ", str(read.exception))
                self.assertGreaterEqual(len(probe.reads), 1, f"the input was held {held * 1e6:.0f} us")
                for entry in probe.reads:
                    self.assertRegex(entry, re.escape(str(probe.input)) + r" (\(control silent\) )?opened for reading ")
                self.assertEqual(([], []), (probe.scanner_opens, probe.errors))
                self.assertEqual("", printed.getvalue())

    def test_a_wake_the_sentinel_has_not_handled_when_the_step_ends_is_still_recorded(self):
        """U625 round 5, from the first container run of the repetition tests (one repetition in twenty lost the
        lever's read): the kernel woke the input's sentinel for the lever's open, but the thread had not run again
        before the step ended, consume() set its stop flag and released it, and the sentinel took the wake for the
        teardown's. The sentinel is held exactly there: os.open is wrapped so that the sentinel's write-open of the
        input, once it has returned, waits until consume() has entered _stop_sentinel for the input (wrapped too,
        to signal), the worst scheduling the kernel allows. The teardown must wait for the wake (the write
        descriptor the kernel installed is in this process's table), so the read is recorded, and nothing is an
        error or a scanner open."""
        import contextlib
        import io
        import threading

        probe = self.worker_root_probe()
        tearing_down, real_open, stop = threading.Event(), os.open, probe._stop_sentinel

        def delayed_open(path, flags, *args, **kwargs):
            fd = real_open(path, flags, *args, **kwargs)
            if os.fspath(path) == os.fspath(probe.input) and flags & os.O_ACCMODE == os.O_WRONLY:
                tearing_down.wait(30)  # the sentinel does not run between the kernel's wake and the teardown
            return fd

        def stopping(fifo):
            if fifo == probe.input:
                tearing_down.set()
            return stop(fifo)

        patched = mock.patch.object(tec.os, "open", delayed_open), mock.patch.object(probe, "_stop_sentinel", stopping)
        with patched[0], patched[1], contextlib.redirect_stderr(io.StringIO()) as printed:
            probe.consume(lambda: in_thread(lambda: os.close(os.open(probe.input, os.O_RDONLY))))
        self.assertTrue(tearing_down.is_set(), "consume() never reached the input's teardown")
        with self.assertRaisesRegex(AssertionError, "worker root: read "):
            probe.assert_untouched()
        self.assertGreaterEqual(len(probe.reads), 1)
        self.assertEqual(([], []), (probe.scanner_opens, probe.errors))
        self.assertEqual("", printed.getvalue())

    def test_an_error_in_the_control_path_during_consume_is_recorded_and_fails_the_check(self):
        """U625 round 4 (verdict of 07efa1d4, P2 f1 s3; AGENTS.md's rule that a safety decision carries a
        failure-injection test): the control FIFO decides scanner versus lever, so a control the probe cannot see
        mid-consume must not pass silently. The consumer removes the control, or puts a regular file or a link in
        its place (by os.replace, so no check sees the control absent), and returns after two further identity
        checks have looked at it (round 5: the control's sentinel is blocked on the FIFO's inode and wakes for no
        rename, so the identity check, an lstat of the name every POLL_S, is what sees the swap; a link is what the
        lstat says it is). Each case is recorded once in `errors` naming the control and the failure, consume()
        itself raises nothing it swallowed (the consumer's own value comes back), assert_untouched fails on the
        entry, and nothing is a read or a scanner open."""
        import contextlib
        import io
        import re

        def removed(control):
            os.unlink(control)

        def regular_file(control):  # os.replace: the control is never absent in between, so one failure is recorded
            control.with_name("swap").write_text("not a fifo\n")
            os.replace(control.with_name("swap"), control)

        def link(control):
            os.symlink(control.with_name("elsewhere"), control.with_name("swap"))
            os.replace(control.with_name("swap"), control)

        cases = (
            ("removed", removed, r"cannot tell whether .* is being read: FileNotFoundError\("),
            ("a regular file", regular_file, r" was another file \(inode \d+, mode -rw-"),
            ("a link", link, r" was another file \(inode \d+, mode l"),
        )
        for name, inject, failure in cases:
            with self.subTest(name):
                probe = self.worker_root_probe()

                def consumer(inject=inject, probe=probe):
                    inject(probe.control)
                    seen = probe.checks
                    while probe.checks < seen + 2:
                        time.sleep(0.001)
                    return "consumed"

                with contextlib.redirect_stderr(io.StringIO()) as printed:
                    self.assertEqual("consumed", probe.consume(consumer))
                self.assertEqual(1, len(probe.errors), probe.errors)
                self.assertRegex(probe.errors[0], re.escape(str(probe.control)))
                self.assertRegex(probe.errors[0], failure)
                with self.assertRaisesRegex(AssertionError, "worker root: ") as failed:
                    probe.assert_untouched()
                self.assertIn(probe.errors[0], str(failed.exception))
                self.assertEqual(([], [], []), (probe.reads, probe.scanner_opens, probe._control_wakes))
                self.assertEqual("", printed.getvalue())

    def test_the_holder_scan_tolerates_a_pid_that_exits_mid_scan(self):
        # Round 1 finding f1 s4: a pid that exits between its fd listing and its field reads answers ESRCH, which
        # escaped the scan and aborted the attempt, losing the read it had already detected. The three fields fail
        # three ways here: comm by permission, status by absence, cmdline by ESRCH itself.
        probe = self.worker_root_probe()
        proc = probe.base / "proc"
        probe.PROC_ROOT = str(proc)
        holder = proc / "4242"
        (holder / "fd").mkdir(parents=True)
        os.symlink(probe.input, holder / "fd" / "7")
        (holder / "comm").write_text("cat\n")
        (holder / "comm").chmod(0o000)
        self.addCleanup((holder / "comm").chmod, 0o600)
        with self.assertRaises(PermissionError):  # root could read it, and the record would name cat instead of ?
            (holder / "comm").read_bytes()
        read_bytes = tec.Path.read_bytes

        def exiting(path, *args, **kwargs):
            if path == holder / "cmdline":
                raise ProcessLookupError(errno.ESRCH, "no such process")
            return read_bytes(path, *args, **kwargs)

        record = "by pid 4242 (?, ppid ?: ?)"
        with mock.patch.object(tec.Path, "read_bytes", exiting):
            self.assertEqual(record, self.holder_scan(probe))
            self.assert_eof(probe.consume(lambda: run(["/bin/cat", str(probe.input)], ALLOWED_ENV)))
        with self.assertRaisesRegex(AssertionError, "worker root: read ") as exited:
            probe.assert_untouched()
        self.assertIn(f"{probe.input} opened for reading {record}", str(exited.exception))
        self.assertEqual([], probe.errors)

    def test_the_holder_scan_opens_no_fifo(self):
        """The scan reads the descriptor table without opening what it finds in it: os.stat follows a /proc fd link to
        its target without opening it. A planted FIFO nobody reads is the witness, because a non-blocking write-open
        answers ENXIO only while the FIFO has no reader, so a poll that lands while the scan runs tells whether the
        scan is a reader. The fd/5 link to the sentinel is the second match that the break names the pid once for.

        U241: the poll landed by scheduler luck. Until d1ecd495 the tree held 500 decoy pids whose fd/3 pointed at the
        FIFO, so that the scan would last long enough for the main thread to poll it once; on a loaded macOS runner the
        scan of 501 pids finished before the main thread ran at all, and the test's own guard failed healthy code with
        `AssertionError: 0 not greater than 0 : no poll landed inside the scan` (run 42167444941, job 127727472511,
        test (macos-15, client), PR 674, 2026-11-06, and another macOS leg at 00:37Z the same day). The decoys are
        gone and the poll is handshaken instead: the per-pid `os.listdir(<root>/<pid>/fd)` of `_holders`
        (trusted_exec_contract.py:255 at d1ecd495) is wrapped to signal `inside` on its first call and wait for
        `polled`, which the main thread sets after its first poll returns nothing opened. The scan cannot pass its
        first pid until a poll has landed inside it, so both guards hold by construction on any scheduler. The hook
        is a directory listing, not the os.stat the test judges, and no open of the test's own touches it."""
        import threading

        probe = self.worker_root_probe()
        probe.consume(lambda: None)
        self.assertEqual([], probe.reads)
        proc, planted = probe.base / "proc", probe.base / "planted.fifo"
        probe.PROC_ROOT = str(proc)
        os.mkfifo(planted, 0o600)
        holder = proc / "4242"
        (holder / "fd").mkdir(parents=True)
        os.symlink(planted, holder / "fd" / "3")
        os.symlink(probe.input, holder / "fd" / "4")
        os.symlink(probe.input, holder / "fd" / "5")  # a second match: the break names the pid once, not twice
        (holder / "comm").write_text("cat\n")
        (holder / "status").write_text("PPid:\t77\n")
        (holder / "cmdline").write_bytes(b"/bin/cat\0" + os.fsencode(probe.input) + b"\0")

        def opened():
            """What the scan has opened for reading, nothing being the empty string."""
            writer = probe._open_writer()
            if writer is not None:
                os.close(writer)
                return "the scan opened the sentinel for reading"
            try:
                os.close(os.open(planted, os.O_WRONLY | os.O_NONBLOCK))
            except OSError as error:
                return "" if error.errno == errno.ENXIO else f"the planted FIFO answered {error!r}"
            return "the scan opened the planted FIFO for reading"

        inside, polled = threading.Event(), threading.Event()
        listdir = tec.os.listdir

        def listing(path, *args, **kwargs):
            """The scan's own listing of a pid's fd directory, held at the first one until a poll has landed."""
            if os.path.basename(path) == "fd" and not inside.is_set():
                inside.set()
                polled.wait(30)
            return listdir(path, *args, **kwargs)

        record, polls = {}, 0
        scan = threading.Thread(target=lambda: record.update(value=probe._holders(None)), daemon=True)
        with mock.patch.object(tec.os, "listdir", listing):
            scan.start()
            inside.wait(30)
            self.assertEqual("", opened())
            polls += 1
            polled.set()
            while scan.is_alive():
                self.assertEqual("", opened())
                polls += 1
            scan.join(30)
        self.assertFalse(scan.is_alive())
        self.assertTrue(inside.is_set(), "the scan never listed a pid's descriptor table")
        self.assertGreater(polls, 0, "no poll landed inside the scan")
        self.assertEqual("", opened())
        self.assertEqual(f"by pid 4242 (cat, ppid 77: /bin/cat {probe.input} )", record["value"])

    def test_the_holder_scan_waits_for_a_reader_whose_open_has_not_returned(self):
        """A scan that names nobody is repeated for HOLDER_WAIT_S before its answer stands, because a reader the
        write-open just woke has no descriptor until its own open() returns (2026-11-04 on the ubuntu-26.04 canary:
        the in-thread reader counted for the write-open while still inside its blocking open(), so its descriptor was
        not in its table when the scan looked, and the record named nobody). The holder here is absent from the
        scan's first pass and present at a later one, built aside and renamed in whole so no pass sees it half made;
        the second probe, whose tree stays empty, proves the wait is HOLDER_WAIT_S long and no longer.

        U241b: the holder used to be renamed in 50 ms after the scan started, on a timer that assumed the scan was
        still walking; on a loaded macOS runner the scan settled before the holder thread ran, and the test failed
        healthy code with `by no process whose descriptors this user can read (0 unreadable)` (the macOS test leg of
        PR 695, 2026-11-06). The holder is handshaken instead, as U241 did for the FIFO test: the scan's listing of
        the proc root (`os.listdir(root)`, trusted_exec_contract.py:247 at 8f31cf5c) is wrapped to take its first
        listing of the empty tree, signal `inside`, and hand that listing back only once `placed` is set, which the
        holder thread does right after its rename. The first pass therefore ends on an empty tree with the holder in
        place, and the rescan names pid 4242, on any scheduler; a scan that stops rescanning fails. Only the rename
        happens inside the settle window, so the holder's build time cannot eat HOLDER_WAIT_S either.

        U241c: the round-1 audit delayed that rename by 300 ms and healthy code failed three times out of three,
        because the hook waits for `placed` inside the scan's first pass while the settle clock is running (`settle =
        time.monotonic() + HOLDER_WAIT_S` is taken before the first pass, trusted_exec_contract.py:279 at 8f31cf5c),
        and an empty pass that ends after `settle` returns without rescanning: the handshake had the production 200 ms
        to complete, a scheduler premise wider than the 50 ms timer but a premise still. The first probe therefore
        runs with its own HOLDER_WAIT_S of 30 s, the bound of the handshake's own waits, so however long the holder
        thread takes to wake and rename, the first pass ends before `settle` and the rescan at POLL_S names pid 4242;
        a scan that stops rescanning still returns the no-holder record at once. The second probe keeps the
        production HOLDER_WAIT_S and alone measures its length."""
        import threading

        probe = self.worker_root_probe()
        probe.HOLDER_WAIT_S = 30.0  # the hook below waits inside the first pass; the settle must stay out of its reach
        proc = probe.base / "proc"
        proc.mkdir()
        probe.PROC_ROOT = str(proc)
        self.assertEqual([], list(proc.iterdir()))
        inside, placed = threading.Event(), threading.Event()
        listdir = tec.os.listdir

        def listing(path, *args, **kwargs):
            """The scan's own listing of the proc root, the first one taken before the holder exists and handed back
            after it is in place."""
            entries = listdir(path, *args, **kwargs)
            if path == probe.PROC_ROOT and not inside.is_set():
                inside.set()
                placed.wait(30)
            return entries

        def late_holder():
            building = proc / "building"  # not numeric, so a pass that lands here skips it
            (building / "fd").mkdir(parents=True)
            os.symlink(probe.input, building / "fd" / "7")
            (building / "comm").write_text("cat\n")
            (building / "status").write_text("Name:\tcat\nPPid:\t77\n")
            (building / "cmdline").write_bytes(b"/bin/cat\0" + os.fsencode(probe.input) + b"\0")
            inside.wait(30)
            os.rename(building, proc / "4242")
            placed.set()

        late = threading.Thread(target=late_holder, daemon=True)
        late.start()
        self.addCleanup(late.join, 5)
        with mock.patch.object(tec.os, "listdir", listing):
            record = self.holder_scan(probe)
        late.join(5)
        self.assertFalse(late.is_alive())
        self.assertTrue(inside.is_set(), "the scan never listed the proc root")
        self.assertTrue(placed.is_set(), "the holder was never renamed in")
        self.assertEqual(f"by pid 4242 (cat, ppid 77: /bin/cat {probe.input} )", record)
        never = self.worker_root_probe()
        (never.base / "proc").mkdir()
        never.PROC_ROOT = str(never.base / "proc")
        started = time.monotonic()
        record = self.holder_scan(never)
        waited = time.monotonic() - started
        self.assertEqual("by no process whose descriptors this user can read (0 unreadable)", record)
        self.assertGreaterEqual(waited, 0.2)
        self.assertLess(waited, 2)

    def test_a_replacement_present_at_a_poll_fails_even_when_restored(self):
        # Audit round 6 of 0b99fa84: a write-open that landed on another file was discarded, so swapping the FIFO out
        # and back during the step passed. The swap is held for two identity checks (round 5: the latch sees opens, not
        # names, so consume() keeps an lstat of both names every POLL_S): a replacement present at a check is in scope;
        # one swapped and restored between two checks is not (see WorkerRoot's docstring).
        for name, swap_in in (
            ("regular file", lambda path: path.write_text(tec.LEGIT)),
            ("another FIFO", lambda path: os.mkfifo(path)),
            ("symlink", lambda path: path.symlink_to("/dev/null")),
        ):
            with self.subTest(name):
                probe = self.worker_root_probe()
                probe.consume(functools.partial(swap_and_restore, probe, swap_in))
                self.assertEqual(probe._identity[probe.input][0], os.lstat(probe.input).st_ino)  # restored
                with self.assertRaisesRegex(AssertionError, r"wrote .* \(replaced\)"):
                    probe.assert_untouched()

    def test_a_writer_to_the_input_never_hangs(self):
        # A writer blocks in its open until a reader comes; the latch is a writer too, so that reader is the deadline's
        # release of the sentinel (its write then fails or is dropped) and consume() returns instead of hanging.
        probe = self.worker_root_probe()
        probe.consume(lambda: run(["/bin/sh", "-c", 'echo x >> "$0"', str(probe.input)], ALLOWED_ENV), deadline=1)
        probe.consume(lambda: open(probe.input, "wb").close(), deadline=1)

    def test_a_consumer_past_its_deadline_fails_instead_of_hanging(self):
        import threading

        probe, forever = self.worker_root_probe(), threading.Event()
        self.addCleanup(forever.set)
        started = time.monotonic()
        with self.assertRaisesRegex(AssertionError, "consumer thread still running after the deadline"):
            probe.consume(forever.wait, deadline=1)
        self.assertLess(time.monotonic() - started, 10)
        self.assertEqual({}, tec._CONSUMER_ERRORS)  # the timed-out worker is not left registered

    def test_a_late_reader_is_recorded_and_a_writer_blocked_past_the_deadline_is_released(self):
        # Until round 4 a reader blocked on the sentinel's open until the deadline's attempt released it. The latch is a
        # writer, so no reader blocks on the input any more: a reader that opens after the step began is recorded at
        # once. What still blocks there is a writer, waiting for a reader: the deadline's release of the sentinel is
        # that reader, so consume() returns then and not before, instead of hanging; the release's own wake is the
        # teardown's, not a read, and a FIFO keeps no content, so the check passes.
        probe = self.worker_root_probe()
        late_reader = lambda: (time.sleep(0.2), Path(probe.input).read_bytes())[1]
        self.assertEqual(b"", probe.consume(late_reader, deadline=1))
        with self.assertRaisesRegex(AssertionError, "worker root: read "):
            probe.assert_untouched()
        probe = self.worker_root_probe()
        started = time.monotonic()
        probe.consume(lambda: open(probe.input, "wb").close(), deadline=1)
        self.assertGreaterEqual(time.monotonic() - started, 1)  # released at the deadline, not before
        self.assertLess(time.monotonic() - started, 10)
        probe.assert_untouched()

    def assert_gone(self, pid, timeout=10):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            time.sleep(0.01)
        self.fail(f"process {pid} is still running after its group was stopped")

    def test_a_descendant_that_ignores_term_and_closed_its_output_is_killed(self):
        # Audit round 10 of 8ae07078: after TERM the shell exits and the pipes close, so a group stop that returned
        # then skipped KILL for a descendant that ignores TERM and had closed its output.
        inner = 'trap "" TERM; echo $$; exec >/dev/null 2>&1; sleep 1000'
        with self.assertRaises(subprocess.TimeoutExpired) as expired:
            run(["/bin/sh", "-c", 'sh -c "$0" & wait', inner], ALLOWED_ENV, timeout=1)
        self.assert_gone(int(expired.exception.output.split()[0]))

    def test_kill_group_accepts_eperm_only_for_a_successful_empty_ps_listing(self):
        # Failure injection for the EPERM decision: KILL to the group answers EPERM, and ps answers (a) a failure,
        # (b) output that cannot be parsed, (c) a live member of the group, or (d) a successful listing with no
        # member of the group (none at all, or zombies only). Only (d) accepts the EPERM; the others raise.
        pgid = 424242

        class Proc:
            pid = pgid

            def communicate(self, timeout=None):
                return b"out", b""

        def killpg(group, sig):
            if sig == signal.SIGKILL:
                raise PermissionError(errno.EPERM, "Operation not permitted")

        def ps(stdout="", returncode=0):
            def fake(argv, **kwargs):
                self.assertEqual("/bin/ps", argv[0])
                if returncode:
                    raise subprocess.CalledProcessError(returncode, argv)
                return subprocess.CompletedProcess(argv, returncode, stdout, "")

            return fake

        cases = (
            ("ps fails", ps(returncode=1), subprocess.CalledProcessError),
            ("ps unparsable", ps(stdout="not a listing\n"), ValueError),
            ("live member", ps(stdout=f"  77 {pgid} S+\n 1 1 Ss\n"), PermissionError),
            ("empty listing", ps(stdout="  1 1 Ss\n"), None),
            ("zombies only", ps(stdout=f"  1 1 Ss\n 78 {pgid} Z\n"), None),
        )
        for name, fake_ps, raised in cases:
            with (
                self.subTest(name),
                mock.patch.object(os, "killpg", killpg),
                mock.patch.object(subprocess, "run", fake_ps),
            ):
                if raised is None:
                    self.assertEqual((b"out", b""), kill_group(Proc()))
                else:
                    with self.assertRaises(raised):
                        kill_group(Proc())

    def test_a_timed_out_subprocess_consumer_leaves_no_descendant(self):
        # A shell whose child blocks on a FIFO nobody serves: at the timeout the whole process group is stopped.
        fifo = self.scratch("trusted-exec-group-") / "fifo"
        os.mkfifo(fifo)
        with self.assertRaises(subprocess.TimeoutExpired) as expired:
            run(["/bin/sh", "-c", 'cat "$0" & echo "$!"; wait', str(fifo)], ALLOWED_ENV, timeout=1)
        self.assert_gone(int(expired.exception.output.split()[0]))

    def test_an_errno_other_than_enxio_fails_the_probe(self):
        # No except-all: the only answers the probe reads are ENXIO (no reader) and ENOENT/ELOOP (removed, replaced).
        probe, real = self.worker_root_probe(), os.open

        def eio(path, flags, *args, **kwargs):
            if os.fspath(path) == os.fspath(probe.input) and flags & os.O_ACCMODE == os.O_WRONLY:
                raise OSError(errno.EIO, "injected I/O error", os.fspath(path))
            return real(path, flags, *args, **kwargs)

        with mock.patch.object(tec.os, "open", eio):
            probe.consume(lambda: None)
        with self.assertRaisesRegex(AssertionError, r"cannot tell whether .* is being read: .*EIO|injected I/O error"):
            probe.assert_untouched()

    def test_a_consumer_exception_is_raised_to_the_caller_and_no_thread_is_left(self):
        import threading

        probe = self.worker_root_probe()
        before = threading.active_count()
        with self.assertRaisesRegex(ValueError, "from the consumer"):
            probe.consume(lambda: (_ for _ in ()).throw(ValueError("from the consumer")))
        self.assertEqual(7, probe.consume(lambda: 7))
        self.assertEqual(before, threading.active_count())
        self.assertEqual({}, tec._CONSUMER_ERRORS)

    def scratch(self, prefix):
        base = Path(tempfile.mkdtemp(prefix=prefix)).resolve()
        self.addCleanup(shutil.rmtree, base, True)
        return base

    def test_the_self_test_refuses_a_probe_whose_reads_would_not_be_seen(self):
        # Synchronous: ENXIO without a reader, success with the probe's own reader, ENXIO again after it closes.
        for name, fake in (
            ("writer never succeeds", lambda self: None),
            ("writer always succeeds", lambda self: os.open(os.devnull, os.O_WRONLY)),
        ):
            with (
                self.subTest(name),
                mock.patch.object(tec.WorkerRoot, "_open_writer", fake),
                self.assertRaises(RuntimeError),
            ):
                tec.WorkerRoot(self.scratch("trusted-exec-selftest-"))
        with (
            mock.patch.object(tec.WorkerRoot, "_open_writer", side_effect=OSError(errno.EIO, "injected")),
            self.assertRaisesRegex(OSError, "injected"),
        ):
            tec.WorkerRoot(self.scratch("trusted-exec-selftest-"))

    def test_worker_root_probe_detects_a_same_length_overwrite(self):
        identity = lambda st: (st.st_ino, st.st_size, st.st_mtime_ns)
        for name in ("output",):  # in place, same length, the mtime put back: what a coarse clock leaves behind
            with self.subTest(name):
                probe = self.worker_root_probe()
                path, st = getattr(probe, name), os.stat(getattr(probe, name))
                with os.fdopen(
                    os.open(path, os.O_WRONLY), "wb"
                ) as handle:  # write-only, no truncation: nothing is read
                    handle.write(tec.LEGIT.upper().encode())
                os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns))
                self.assertEqual(identity(st), identity(os.stat(path)), "precondition: inode, size, mtime unchanged")
                with self.assertRaisesRegex(AssertionError, "wrote "):
                    probe.assert_untouched()

    def test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check(self):
        entry = pwd.struct_passwd(("probe", "*", uid := os.getuid(), 20, "Probe", "/home/probe", "/bin/sh"))
        relative = pwd.struct_passwd(entry[:5] + ("probe", "/bin/sh"))  # a passwd home that is not absolute
        dscl = ["/usr/bin/dscl", ".", "-read", "/Users/probe", "NFSHomeDirectory"]
        getent, ds = ["/usr/bin/getent", "passwd", str(uid)], "_directory_service"
        refused = subprocess.CalledProcessError(70, dscl)  # what both seat sandboxes answer for dscl
        for platform, argv, answer, outcome in (  # outcome: the home returned, or the refusal's reason
            ("darwin", dscl, "NFSHomeDirectory: /home/probe\n", "/home/probe"),
            ("darwin", dscl, "NFSHomeDirectory:\n /home/probe\n", "/home/probe"),
            ("darwin", dscl, refused, "/home/probe"),
            ("darwin", dscl, "NFSHomeDirectory: /Users/other\n", "disagree"),
            ("darwin", dscl, "No such key: NFSHomeDirectory\n", "disagree"),
            ("linux", getent, f"probe:*:{uid}:20:Probe:/home/probe:/bin/sh\n", "/home/probe"),
            ("linux", getent, OSError("no getent"), "/home/probe"),
            ("linux", getent, "a:b\n", "disagree"),
            ("win32", None, None, "/home/probe"),
            ("win32", None, None, "no absolute"),
        ):
            side = {"side_effect": answer} if isinstance(answer, BaseException) else {"return_value": answer}
            with self.subTest(f"{platform} {answer!r} {outcome}"), mock.patch.object(sys, "platform", platform):
                with (
                    mock.patch.object(tec.pwd, "getpwuid", return_value=relative if "absolute" in outcome else entry),
                    mock.patch.object(tec, ds, **side) as service,
                ):
                    if outcome.startswith("/"):
                        self.assertEqual(outcome, tec.passwd_home())
                    else:
                        self.assertRaisesRegex(RuntimeError, outcome, tec.passwd_home)
                self.assertEqual(argv, service.call_args.args[0] if service.call_args else None)

    def test_probes_clean_up_after_an_exception(self):
        before = dict(os.environ)
        for factory in (tec.shim_path, tec.hostile_git, tec.worker_root, tec.swapped_file):
            with self.subTest(factory.args[0].__name__):
                with self.assertRaises(RuntimeError), factory() as probe:
                    base = probe.base
                    raise RuntimeError("deliberate")
                self.assertFalse(base.exists())
        self.assertEqual(before, dict(os.environ))
