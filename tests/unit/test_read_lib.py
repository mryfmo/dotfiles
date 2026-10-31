#!/usr/bin/env python3
"""Exercise scripts/orchestrator/read-lib.sh, the fail-closed readers the levers source (regime-cutover U112, P-21).

Each reader runs under /bin/bash (3.2 on macOS, the shell four of the five levers get through `#!/usr/bin/env bash`
there) in a scratch HOME, with the fake git of tests/unit/test_pr_levers.py first on PATH where a git failure is
injected. The tests assert the three outcomes a caller sees: 0 with the value, 1 with an empty variable and nothing
printed, 2 with one stderr line naming the key, the file or the producer and the status; and that the reader returns
in every case, so the script after it goes on.

INJECTIONS lists every reader the library defines with the test that injects its producer's failure. The suite holds
the list to the `read_*` functions the sourced library defines, and each named test to the injection it makes
(FAKE_GIT_FAIL, FAKE_GIT_WARN or a mode-000 path), so a reader added without such a test fails the suite.
"""

from __future__ import annotations

import inspect
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scratch_git import git_init  # noqa: E402
from test_pr_levers import GIT_WRAPPER  # noqa: E402

LIB = ROOT / "scripts/orchestrator/read-lib.sh"
BASH = "/bin/bash" if Path("/bin/bash").is_file() else "bash"
INJECTIONS = {
    "read_config": "ReadConfigTest.test_a_failed_git_config_is_never_read_as_unset",
    "read_listing": "ReadListingTest.test_a_producer_that_fails_or_warns_is_a_failed_read",
    "read_file": "ReadFileTest.test_a_missing_or_unreadable_file_is_a_failed_read_naming_the_path",
}
INJECTION_MARKS = ("FAKE_GIT_FAIL", "FAKE_GIT_WARN", "chmod(0o000)")
UNREADABLE_DIR = "warning: could not open directory"  # git 2.56.0's line for a mode-000 directory under the pathspec


class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="read-lib-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home"
        self.home.mkdir()
        bindir = self.root / "bin"
        bindir.mkdir()
        wrapper = bindir / "git"
        wrapper.write_text(GIT_WRAPPER)
        wrapper.chmod(0o755)
        (self.home / ".gitconfig").write_text("[user]\n\tname = t\n\temail = t@example.invalid\n")
        self.env = {
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "HOME": str(self.home),
            "LC_ALL": "C",
            "REAL_GIT": shutil.which("git"),
            "GIT_CONFIG_GLOBAL": str(self.home / ".gitconfig"),
            "GIT_CONFIG_NOSYSTEM": "1",
        }

    def reader(self, call, after="", env=None, cwd=None):
        """Source the library, run one reader call and print its status, then `after`: the script ends with status 0
        whatever the reader returned, which is the "no reader exits" half of the contract."""
        script = f'. "{LIB}"\nstatus=0\n{call} || status=$?\nprintf "status=%s\\n" "${{status}}"\n{after}'
        run = subprocess.run(
            [BASH, "-c", script],
            env=env or self.env,
            cwd=cwd or self.root,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(run.returncode, 0, "the reader returned and the script went on:\n" + run.stdout + run.stderr)
        return run

    def git(self, *args, cwd=None):
        subprocess.run(
            [self.env["REAL_GIT"], *args], cwd=cwd or self.root, env=self.env, check=True, capture_output=True
        )

    def repo(self):
        """A scratch repository with a committed file under a/b and an untracked one beside it."""
        repo = self.root / "repo"
        (repo / "a/b").mkdir(parents=True)
        (repo / "a/b/tracked").write_text("1\n")
        (repo / "a/b/untracked").write_text("2\n")
        git_init(repo, env=self.env)
        self.git("add", "a/b/tracked", cwd=repo)
        self.git("commit", "-q", "-m", "base", cwd=repo)
        return repo

    def assert_one_line(self, stderr, *fragments):
        self.assertEqual(stderr.count("\n"), 1, stderr)
        for fragment in fragments:
            self.assertIn(fragment, stderr)


class ReaderTableTest(unittest.TestCase):
    def test_every_reader_the_library_defines_has_an_injection_test(self):
        run = subprocess.run(
            [BASH, "-c", f'. "{LIB}" && declare -F'],
            env={"PATH": os.environ["PATH"], "HOME": os.environ.get("HOME", "/"), "LC_ALL": "C"},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        readers = {line.split()[-1] for line in run.stdout.splitlines() if line.split()[-1].startswith("read_")}
        self.assertEqual(set(INJECTIONS), readers, "a reader without a row, or a row without a reader")
        for test in INJECTIONS.values():
            cls, _, method = test.partition(".")
            function = getattr(globals()[cls], method, None)
            self.assertTrue(callable(function), f"{test} does not exist")
            source = inspect.getsource(function)
            self.assertTrue(
                any(mark in source for mark in INJECTION_MARKS), f"{test} injects none of {INJECTION_MARKS}"
            )


class ReadConfigTest(ReaderTest):
    def test_a_set_key_is_its_value_and_an_unset_or_empty_key_is_absent(self):
        err = self.root / "config.err"
        show = 'printf "value=[%s]\\n" "${v}"'
        run = self.reader(f'read_config git user.name v "{err}"', show)
        self.assertEqual((run.stdout, run.stderr), ("status=0\nvalue=[t]\n", ""))
        run = self.reader(f'read_config git user.absent v "{err}"', show)
        self.assertEqual((run.stdout, run.stderr), ("status=1\nvalue=[]\n", ""))
        self.git("config", "--global", "user.empty", "")
        run = self.reader(f'read_config git user.empty v "{err}"', show)
        self.assertEqual((run.stdout, run.stderr), ("status=1\nvalue=[]\n", ""))
        # The variable named is the one written, whatever it held before.
        run = self.reader(f'v=stale\nread_config git user.absent v "{err}"', show)
        self.assertEqual(run.stdout, "status=1\nvalue=[]\n")

    def test_a_failed_git_config_is_never_read_as_unset(self):
        """git 2.56.0 (research 01 section 1.2): 128 for an unparsable file, 3 in the manual, and 1 with only a
        warning for an unreadable `-f` file, the status of an unset key. Each is a 2 naming the key and the status."""
        err = self.root / "config.err"
        show = 'printf "value=[%s]\\n" "${v}"'
        cases = {
            "exit 3": ({"FAKE_GIT_FAIL": "config", "FAKE_GIT_FAIL_STATUS": "3"}, "(git config exited 3)"),
            "exit 128": ({"FAKE_GIT_FAIL": "config", "FAKE_GIT_FAIL_STATUS": "128"}, "(git config exited 128)"),
            "exit 1 with a warning": ({"FAKE_GIT_WARN": "config"}, "(git config exited 1); it wrote to its stderr"),
        }
        for name, (injected, message) in cases.items():
            with self.subTest(name):
                run = self.reader(f'read_config git user.name v "{err}"', show, env={**self.env, **injected})
                self.assertEqual(run.stdout, "status=2\nvalue=[]\n")
                self.assert_one_line(run.stderr, "read_config: cannot read git config user.name", message)
                self.assertNotIn("unset", run.stderr)
        # A warning beside a value and exit 0 is a failed read too: the stderr file decides, whatever the status.
        warned = 'warned_git() { echo "warning: planted" >&2; echo value; }\n'
        run = self.reader(warned + f'read_config warned_git user.name v "{err}"', show)
        self.assertEqual(run.stdout, "status=2\nvalue=[]\n")
        self.assert_one_line(run.stderr, "(git config exited 0); it wrote to its stderr")
        # A stderr file that cannot be written is a failed read, never "unset" by an absent file.
        run = self.reader(f'read_config git user.name v "{self.root}/absent/config.err"', show)
        self.assertEqual(run.stdout, "status=2\nvalue=[]\n")
        self.assert_one_line(run.stderr, "cannot write", "user.name")

    @unittest.skipIf(os.geteuid() == 0, "file modes do not bind root")
    def test_the_measured_unreadable_file_shape_with_the_real_git(self):
        """The real git on a mode-000 `-f` file: exit 1 with a warning, read as a failure."""
        config = self.root / "u.cfg"
        config.write_text("[a]\n\tb = 1\n")
        config.chmod(0o000)
        self.addCleanup(config.chmod, 0o644)
        err = self.root / "config.err"
        # `"$1" config --get key` with the file: the function drops the `config` word and re-adds it with -f.
        unreadable = f'file_git() {{ shift; "{self.env["REAL_GIT"]}" config -f "{config}" "$@"; }}\n'
        run = self.reader(unreadable + f'read_config file_git a.b v "{err}"', 'printf "value=[%s]\\n" "${v}"')
        self.assertEqual(run.stdout, "status=2\nvalue=[]\n")
        self.assert_one_line(run.stderr, "cannot read git config a.b (git config exited 1); it wrote to its stderr")
        self.assertIn("unable to access", err.read_text())


class ReadListingTest(ReaderTest):
    def test_the_listing_is_written_to_the_file_and_an_empty_one_is_absent(self):
        out, err = self.root / "out", self.root / "err"
        run = self.reader(f'read_listing "{out}" "{err}" printf "a\\0b\\0"')
        self.assertEqual((run.stdout, run.stderr), ("status=0\n", ""))
        self.assertEqual((out.read_bytes(), err.read_bytes()), (b"a\0b\0", b""))
        run = self.reader(f'read_listing "{out}" "{err}" true')
        self.assertEqual((run.stdout, run.stderr), ("status=1\n", ""))
        self.assertEqual(out.read_bytes(), b"", "the output file is truncated first")
        lister = 'lister() { printf "%s\\n" "$@"; }\n'
        run = self.reader(lister + f'read_listing "{out}" "{err}" lister x y')
        self.assertEqual((run.stdout, out.read_text()), ("status=0\n", "x\ny\n"), "a function is a producer too")

    def test_a_producer_that_fails_or_warns_is_a_failed_read(self):
        out, err = self.root / "out", self.root / "err"
        repo = self.repo()
        ls_files = "git ls-files -z --cached --others --exclude-standard -- ."
        cases = {
            "exits nonzero after printing": ('sh -c "echo partial; exit 3"', {}, "read_listing: sh -c exited 3"),
            "cannot be run": ("no-such-producer-u112 -x", {}, "no-such-producer-u112 -x exited 127"),
            "warns and exits 0": ('sh -c "echo warned >&2; echo out"', {}, "sh -c exited 0 and wrote to its stderr"),
            "FAKE_GIT_FAIL after output": (ls_files, {"FAKE_GIT_FAIL_AFTER": "ls-files"}, "git ls-files exited 1"),
            "FAKE_GIT_FAIL": (ls_files, {"FAKE_GIT_FAIL": "ls-files", "FAKE_GIT_FAIL_STATUS": "128"}, "exited 128"),
        }
        for name, (producer, injected, message) in cases.items():
            with self.subTest(name):
                run = self.reader(f'read_listing "{out}" "{err}" {producer}', env={**self.env, **injected}, cwd=repo)
                self.assertEqual(run.stdout, "status=2\n")
                self.assert_one_line(run.stderr, message)
        run = self.reader(f'read_listing "{out}" "{err}"')
        self.assertEqual(run.stdout, "status=2\n")
        self.assert_one_line(run.stderr, "no producer named")
        run = self.reader(f'read_listing "{self.root}/absent/out" "{err}" true')
        self.assertEqual(run.stdout, "status=2\n")
        self.assert_one_line(run.stderr, "cannot write")

    @unittest.skipIf(os.geteuid() == 0, "file modes do not bind root")
    def test_the_measured_git_ls_files_warning_with_exit_0_is_a_failed_read(self):
        """Research 01 section 1.1 on the real git: a mode-000 directory under the pathspec warns, exits 0 and drops
        its untracked files; the stderr file makes it a 2, so no file is read as deleted."""
        repo = self.repo()
        locked = repo / "a/b"
        locked.chmod(0o000)
        self.addCleanup(locked.chmod, 0o755)
        out, err = self.root / "out", self.root / "err"
        run = self.reader(
            f'read_listing "{out}" "{err}" git ls-files -z --cached --others --exclude-standard -- .', cwd=repo
        )
        self.assertEqual(run.stdout, "status=2\n")
        self.assert_one_line(run.stderr, "read_listing: git ls-files exited 0 and wrote to its stderr")
        self.assertIn(UNREADABLE_DIR, err.read_text())
        self.assertIn(b"a/b/tracked\0", out.read_bytes(), "git printed the cached entry and exited 0 all the same")


class ReadFileTest(ReaderTest):
    def test_the_whole_file_is_read_with_its_trailing_newlines_and_an_empty_file_is_absent(self):
        path = self.root / "text"
        path.write_text("a\n\n\n")
        show = 'printf "[%s]" "${v}"'
        run = self.reader(f'read_file "{path}" v', show)
        self.assertEqual((run.stdout, run.stderr), ("status=0\n[a\n\n\n]", ""))
        path.write_text("")
        run = self.reader(f'v=stale\nread_file "{path}" v', show)
        self.assertEqual((run.stdout, run.stderr), ("status=1\n[]", ""))

    def test_a_missing_or_unreadable_file_is_a_failed_read_naming_the_path(self):
        show = 'printf "[%s]" "${v}"'
        missing = self.root / "missing"
        run = self.reader(f'v=stale\nread_file "{missing}" v', show)
        self.assertEqual(run.stdout, "status=2\n[]")
        self.assert_one_line(run.stderr, f"read_file: no file at {missing}")
        directory = self.root / "dir"
        directory.mkdir()
        run = self.reader(f'read_file "{directory}" v', show)
        self.assertEqual(run.stdout, "status=2\n[]")
        self.assert_one_line(run.stderr, f"read_file: cannot read {directory} (cat exited 1)")
        if os.geteuid() != 0:
            locked = self.root / "locked"
            locked.write_text("secret\n")
            locked.chmod(0o000)
            self.addCleanup(locked.chmod, 0o644)
            run = self.reader(f'read_file "{locked}" v', show)
            self.assertEqual(run.stdout, "status=2\n[]")
            self.assert_one_line(run.stderr, f"read_file: cannot read {locked} (cat exited 1)")
            self.assertNotIn("secret", run.stdout + run.stderr)
        # A cat that fails midway: the bytes it printed are not the file.
        cut = self.root / "cut"
        cut.write_text("line 1\nline 2\n")
        fakes = self.root / "fakes"
        fakes.mkdir()
        (fakes / "cat").write_text('#!/bin/sh\n/usr/bin/head -c 3 "$2"\nexit 1\n')
        (fakes / "cat").chmod(0o755)
        env = {**self.env, "PATH": f"{fakes}:{self.env['PATH']}"}
        run = self.reader(f'read_file "{cut}" v', show, env=env)
        self.assertEqual(run.stdout, "status=2\n[]")
        self.assert_one_line(run.stderr, f"read_file: cannot read {cut} (cat exited 1)")


if __name__ == "__main__":
    unittest.main()
