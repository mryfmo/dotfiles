"""Exercise tests/unit/trusted_exec_contract.py: each probe fails for the intended reason on a noncompliant consumer stub
(so an inert attack or a no-op assertion fails the test), then passes a compliant one; fixtures are temporary."""

import errno
import functools
import hashlib
import os
import pwd
import shutil
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


def run(argv, env, timeout=60, **kw):
    """A subprocess with a deadline: one that hangs (a watcher that stopped serving the FIFO) fails the test."""
    return subprocess.run(
        argv, env=env, capture_output=True, check=False, stdin=subprocess.DEVNULL, timeout=timeout, **kw
    )


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
    """Move the input FIFO aside, put SWAP_IN's file in its place until the probe made two attempts, put it back."""
    aside = probe.base / "aside"
    os.rename(probe.input, aside)
    swap_in(probe.input)
    seen = probe.attempts
    while probe.attempts < seen + 2:
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

    def test_a_replacement_present_at_a_poll_fails_even_when_restored(self):
        # Audit round 6 of 0b99fa84: a write-open that landed on another file was discarded, so swapping the FIFO out
        # and back during the step passed. The swap is held for two probe attempts: a replacement present at a poll is
        # in scope; one swapped and restored between two polls is not (see WorkerRoot's docstring).
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
        # A writer blocked on the open is released by the probe's next attempt (its write then fails or is dropped).
        probe = self.worker_root_probe()
        probe.consume(lambda: run(["/bin/sh", "-c", 'echo x >> "$0"', str(probe.input)], ALLOWED_ENV))
        probe.consume(lambda: open(probe.input, "wb").close())

    def test_a_consumer_past_its_deadline_fails_instead_of_hanging(self):
        import threading

        probe, forever = self.worker_root_probe(), threading.Event()
        self.addCleanup(forever.set)
        started = time.monotonic()
        with self.assertRaisesRegex(AssertionError, "still running after its deadline: it hung"):
            probe.consume(forever.wait, deadline=1)
        self.assertLess(time.monotonic() - started, 10)
        self.assertEqual({}, tec._CONSUMER_ERRORS)  # the timed-out worker is not left registered

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
