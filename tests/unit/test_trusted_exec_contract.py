"""Exercise tests/unit/trusted_exec_contract.py, the shared probes of design-quality 5.14 item 7.

Each probe meets a deliberately noncompliant consumer stub, whose probe assertion must fail for the intended reason
(an inert attack or a no-op assertion fails the test), then a compliant stub, which must pass; each case returns the
failure text for the validation record. Fixtures are temporary; no test reads the real home or this repo's Git config.
"""

import hashlib
import os
import pwd
import subprocess
import sys
import tempfile
import threading
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
ATTACKS = (
    ("environment", "attacker root"),
    ("local-worktree", "attacker root"),
    ("local-include", "attacker hook ran"),
)


def run(argv, env, **kw):
    return subprocess.run(argv, env=env, capture_output=True, check=False, stdin=subprocess.DEVNULL, **kw)


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
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as handle:
        data = handle.read()
    if hashlib.sha256(data).hexdigest() != sha:
        raise ValueError("check failed")
    between()
    return data


class TrustedExecContractTest(tec.TrustedExecContractMixin, unittest.TestCase):
    def runner_fixture(self):
        """A fixture root whose script records its argv and its children's environment; the directory-service
        response and the root discovery are the only substitutions."""
        base = Path(self.enter(tempfile.TemporaryDirectory)).resolve()
        root, home, out = base / "root", base / "home", base / "out"
        for d in (root / "scripts", home, out):
            d.mkdir(parents=True)
        script = root / "scripts" / "observe.sh"
        script.write_text(f'printf "%s\\0" "$0" "$@" > "{out}/argv"\n/usr/bin/env -0 > "{out}/env"\n')
        linux = f"me:x:{os.getuid()}:0::{home}:/bin/sh\n"
        response = f"NFSHomeDirectory: {home}\n" if sys.platform == "darwin" else linux
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
        naive_io(probe)
        with self.assertRaisesRegex(AssertionError, "worker root: read .*; wrote .*; created ") as red:
            probe.assert_untouched()
        clean = self.worker_root_probe()
        with self.assertRaises(PermissionError):
            guarded_io(clean)
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
        result = tec.run_under_trusted_parent(fx.script, *ARGS)
        self.assertEqual(0, result.returncode, result.stderr)
        fx.check(ARGS)
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
        with probe.attack("local-worktree") as env:  # the local attack alone, in an environment without GIT_*
            self.assertFalse([k for k in env if k.startswith("GIT_")])
            self.assertIn("worktree", (probe.legit / ".git" / "config").read_text())
        self.assertEqual(before, config())

    def test_worker_root_probe(self):
        self.case_worker_root()
        for name, act, reason in (
            ("read", lambda p: Path(p.input).read_text(), "read "),
            ("wrote", lambda p: Path(p.output).write_text("x"), "wrote "),
            ("created", lambda p: (Path(p.new_output).parent.mkdir(), Path(p.new_output).write_text("x")), "created "),
        ):
            with self.subTest(name):
                probe = self.worker_root_probe()
                self.assertIn("/.claude/worktrees/", str(probe.input))
                self.assertFalse(Path(probe.new_output).exists())
                act(probe)
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
        allowed = ALLOWED_ENV
        tec.assert_sanitized_env(allowed | {"SHLVL": "1"}, declared=("SHLVL",))
        for observed, declared, reason in (
            ({"PATH": "/usr/bin:/bin", "HOME": "/h"}, (), r"missing: \['LANG'\]"),
            (allowed | {"PATH": "/usr/local/bin:/usr/bin:/bin"}, (), "PATH is"),
            (allowed | {"SHLVL": "1"}, (), r"undeclared: \['SHLVL'\]"),
            (allowed, ("SHLVL",), r"missing: \['SHLVL'\]"),
        ):
            with self.subTest(reason), self.assertRaisesRegex(AssertionError, reason):
                tec.assert_sanitized_env(observed, declared)

    def test_trusted_parent_probe(self):
        self.case_trusted_parent()
        fx = self.runner_fixture()
        env = {"PATH": "/usr/bin:/bin", "HOME": str(fx.home), "LANG": "C.UTF-8"}
        run(["/bin/bash", "-c", f"/bin/bash {fx.script} " + " ".join(ARGS[:2])], env, cwd=fx.base)  # word-split argv
        with self.assertRaisesRegex(AssertionError, "argv"):
            fx.check(ARGS[:2])
        outside = fx.base / "outside"
        outside.mkdir()
        (outside / "x.sh").write_text(f'echo ran > "{fx.out}/marker"\n')
        (fx.root.parent / "root-evil").mkdir()
        (fx.root.parent / "root-evil" / "x.sh").write_text(f'echo ran > "{fx.out}/marker"\n')
        (fx.root / "link.sh").symlink_to(outside / "x.sh")
        for name, script in (
            ("relative", "scripts/observe.sh"),
            ("traversal", f"{fx.root}/../outside/x.sh"),
            ("sibling-prefix", f"{fx.root}-evil/x.sh"),
            ("symlink escape", f"{fx.root}/link.sh"),
            ("directory", f"{fx.root}/scripts"),
            ("missing", f"{fx.root}/scripts/none.sh"),
        ):
            with self.subTest(name), self.assertRaises(tec.TrustedExecRefused):
                tec.run_under_trusted_parent(script)
            self.assertFalse((fx.out / "marker").exists())

    def test_passwd_home_reads_the_directory_service_of_each_platform(self):
        name, uid = pwd.getpwuid(os.getuid()).pw_name, os.getuid()
        dscl = ["/usr/bin/dscl", ".", "-read", f"/Users/{name}", "NFSHomeDirectory"]
        getent, entry = ["/usr/bin/getent", "passwd", str(uid)], f"{name}:x:{uid}:20:Probe:/home/probe:/bin/bash\n"
        for platform, argv, response, home in (
            ("darwin", dscl, "NFSHomeDirectory: /Users/probe\n", "/Users/probe"),
            ("darwin", dscl, "NFSHomeDirectory:\n /Users/long name\n", "/Users/long name"),
            ("linux", getent, entry, "/home/probe"),
        ):
            with (
                self.subTest(response),
                mock.patch.object(sys, "platform", platform),
                mock.patch.object(tec, "_directory_service", return_value=response) as service,
            ):
                self.assertEqual(home, tec.passwd_home())
                service.assert_called_once_with(argv)
        for platform, response in (("darwin", "No such key: NFSHomeDirectory\n"), ("linux", "a:b\n"), ("win32", "")):
            with (
                self.subTest(platform),
                mock.patch.object(sys, "platform", platform),
                mock.patch.object(tec, "_directory_service", return_value=response),
                self.assertRaises(RuntimeError),
            ):
                tec.passwd_home()

    def test_probes_clean_up_after_an_exception(self):
        before = dict(os.environ)
        for factory in (tec.shim_path, tec.hostile_git, tec.worker_root, tec.swapped_file):
            with self.subTest(factory.args[0].__name__):
                with self.assertRaises(RuntimeError), factory() as probe:
                    base = probe.base
                    raise RuntimeError("deliberate")
                self.assertFalse(base.exists())
        self.assertFalse([t for t in threading.enumerate() if t.name == "worker-root-probe"])
        self.assertEqual(before, dict(os.environ))
