"""Exercise scripts/orchestrator/sweep-scope.py (regime-cutover U597, the operator's sweep rule C of 2026-11-18): the
one predicate `sweep_required(paths)` over the four path classes (`credential`, `policy`, `lever`,
`deployed-executable`, one frozen tuple of prefixes each, in that precedence), a mixed head's class, a docs-only head
that requires nothing, and the CLI forms pr-merge.sh and the coordinator run under `python3 -I -S`: `<base> <head>`
(the paths `git diff --name-only --no-renames <base>...<head>` lists) and `--stdin` (the paths one per line, as `gh pr
diff <pr> --name-only` prints them), each printing `required <class>` or `not-required`, and exit 2 with one stderr
line on a failed git read, an empty listing, a path git would not list, or usage (standing order 21: never
`not-required` by failure)."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
READER = ROOT / "scripts/orchestrator/sweep-scope.py"
LEVER = ROOT / "scripts/orchestrator/pr-merge.sh"
# One path per class as the AGENTS.md sweep bullet names them.
CREDENTIAL = "home/dot_local/bin/common/executable_hcom-seat"
POLICY = "home/dot_agents/omp/policies/worker.yml"
LEVER_PATH = "scripts/orchestrator/pr-merge.sh"
DEPLOYED = "install/bootstrap.sh"
DOCS = ("docs/plan.md", "README.md", "tests/unit/test_x.py", ".github/workflows/test.yml", "Makefile")


def load_reader():
    """The module imported from beside the levers, as a test of its predicate reads it."""
    spec = importlib.util.spec_from_file_location("sweep_scope", READER)
    module = importlib.util.module_from_spec(spec)
    sys.modules["sweep_scope"] = module
    spec.loader.exec_module(module)
    return module


class SweepScopePredicateTest(unittest.TestCase):
    def setUp(self):
        self.reader = load_reader()

    def test_the_classes_are_frozen_tuples_in_the_order_of_precedence(self):
        self.assertEqual(
            self.reader.CLASS_NAMES, ("credential", "policy", "lever", "deployed-executable"), "the precedence"
        )
        for name, prefixes in self.reader.CLASSES:
            with self.subTest(name):
                self.assertIsInstance(prefixes, tuple)
                self.assertTrue(prefixes, "a class has at least one prefix")
                self.assertRegex(name, r"^[a-z][a-z-]*$", "the class is one lowercase word, as the lever reads it")
                for prefix in prefixes:
                    self.assertNotIn("//", prefix)
                    self.assertFalse(prefix.startswith("/"))

    def test_each_prefix_of_each_class_puts_a_path_in_that_class(self):
        """A representative under each prefix (the prefix itself for an exact entry, a child for a directory) falls
        in its own class: no entry is shadowed by an earlier class."""
        for name, prefixes in self.reader.CLASSES:
            for prefix in prefixes:
                path = prefix + "x" if prefix.endswith("/") else prefix
                with self.subTest(path):
                    self.assertEqual(self.reader.path_class(path), name)
                    self.assertEqual(self.reader.sweep_required([path]), name)
                    self.assertEqual(self.reader.answer([path]), f"required {name}")

    def test_the_classes_of_the_brief(self):
        """The brief's classes: lever (`scripts/orchestrator/`, `home/dot_local/bin/common/`), policy
        (`home/dot_agents/omp/policies/`, the manifest file), credential handling (the four seat levers in both
        places and `home/.chezmoiscripts/`), deployed executables (`home/dot_local/bin/`, `home/dot_dsh/plugins/`,
        `install/`)."""
        for path, name in (
            ("scripts/orchestrator/ledger.py", "lever"),
            ("scripts/orchestrator/README.md", "lever"),
            ("home/dot_local/bin/common/executable_pr-merge.sh", "lever"),
            ("home/dot_agents/omp/policies/orchestrator.yml", "policy"),
            ("home/dot_agents/agent-config.yaml", "policy"),
            ("scripts/orchestrator/hcom-seat", "credential"),
            ("scripts/orchestrator/acp-broker", "credential"),
            ("scripts/orchestrator/seat-token-place", "credential"),
            ("scripts/orchestrator/seat-login-preflight", "credential"),
            ("home/dot_local/bin/common/executable_hcom-seat", "credential"),
            ("home/dot_local/bin/common/executable_acp-broker", "credential"),
            ("home/dot_local/bin/common/executable_seat-token-place", "credential"),
            ("home/dot_local/bin/common/executable_seat-login-preflight", "credential"),
            ("home/.chezmoiscripts/run_once_before_10-install.sh.tmpl", "credential"),
            ("home/dot_local/bin/executable_tool", "deployed-executable"),
            ("home/dot_dsh/plugins/thak/index.js", "deployed-executable"),
            ("install/bootstrap.sh", "deployed-executable"),
        ):
            with self.subTest(path):
                self.assertEqual(self.reader.path_class(path), name)

    def test_a_mixed_head_takes_the_first_class_in_precedence(self):
        self.assertEqual(self.reader.sweep_required([*DOCS, LEVER_PATH]), "lever")
        self.assertEqual(self.reader.sweep_required([LEVER_PATH, CREDENTIAL]), "credential")
        self.assertEqual(self.reader.sweep_required([DEPLOYED, LEVER_PATH]), "lever")
        self.assertEqual(self.reader.sweep_required([DEPLOYED, POLICY, *DOCS]), "policy")
        self.assertEqual(self.reader.sweep_required([*DOCS, DEPLOYED]), "deployed-executable")
        self.assertEqual(self.reader.answer([*DOCS, DEPLOYED]), "required deployed-executable")

    def test_a_head_outside_every_class_requires_nothing(self):
        """Docs, tests, CI scripts and workflows, the Makefile, a sibling whose name only starts with a prefix, the
        manifest's neighbours and a prefix without its slash are no class."""
        outside = (
            *DOCS,
            "scripts/ci/run-on-lint-files.sh",
            "scripts/generate-agent-configs.py",
            "scripts/orchestratorx/a.sh",
            "scripts/orchestrator",
            "home/dot_agents/agent-config.yaml.bak",
            "home/dot_agents/permgate-policy.yaml",
            "home/dot_local/binx/a",
            "home/dot_local/share/a",
            "install",
            "installer/a.sh",
            "home/dot_dsh/profiles/thak/package.json",
            "home/chezmoiscripts/a",
        )
        for path in outside:
            with self.subTest(path):
                self.assertIsNone(self.reader.path_class(path))
        self.assertIsNone(self.reader.sweep_required(outside))
        self.assertEqual(self.reader.answer(outside), "not-required")

    def test_the_lever_reads_this_module_from_the_checkout_on_stdin(self):
        """pr-merge.sh names the module by its checkout path and runs its `--stdin` form over `gh pr diff
        --name-only`, and prints the one skip line (U597)."""
        text = LEVER.read_text()
        self.assertIn("scope_reader=${toplevel}/scripts/orchestrator/sweep-scope.py", text)
        self.assertIn('"${scope_reader}" --stdin <<< "${paths}"', text)
        self.assertIn('gh_bounded pr diff "${pr}" --name-only', text)
        self.assertIn("sweep: not required (no lever, policy, credential or deployed-executable path changed)", text)
        self.assertEqual(text.count("require_sweep_scope\n"), 1, "called once")
        self.assertIn("[[ -z ${sweep_class} ]] || require_sweep_row\n", text)


class SweepScopeCliTest(unittest.TestCase):
    """The CLI as pr-merge.sh and the coordinator run it, `python3 -I -S sweep-scope.py ...`, in a scratch
    repository with a base commit and heads that change docs, a lever and a credential lever."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n")
        self.env = quiet_git_env(
            {
                "PATH": os.environ["PATH"],
                "HOME": str(self.root / "home"),
                "LC_ALL": "C",
                "GIT_CONFIG_GLOBAL": str(gitconfig),
                "GIT_CONFIG_NOSYSTEM": "1",
            }
        )
        (self.root / "home").mkdir()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git_init(self.repo, env=self.env)
        for path in (*DOCS, LEVER_PATH, CREDENTIAL, "scripts/orchestrator/old.py"):
            self.write(path, "base\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")
        self.base = self.git("rev-parse", "HEAD")
        self.docs_head = self.head("docs", {DOCS[0]: "docs\n", DOCS[2]: "tests\n"})
        self.lever_head = self.head("lever", {LEVER_PATH: "lever\n", DOCS[0]: "docs\n"})
        self.mixed_head = self.head("mixed", {LEVER_PATH: "lever\n", CREDENTIAL: "seat\n", DOCS[1]: "readme\n"})

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.repo, env=self.env, check=True, capture_output=True, text=True
        ).stdout.strip()

    def head(self, name, changes):
        """A branch `name` off the base with `changes` committed; returns its sha, main checked out again."""
        self.git("switch", "-q", "-c", name, self.base)
        for path, text in changes.items():
            self.write(path, text)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", name)
        sha = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        return sha

    def run_reader(self, *args, cwd=None, stdin=None):
        return subprocess.run(
            [sys.executable, "-I", "-S", str(READER), *args],
            cwd=cwd or self.repo,
            env=self.env,
            input=stdin,
            capture_output=True,
            timeout=60,
            check=False,
        )

    def assert_answer(self, run, answer):
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, f"{answer}\n".encode(), b""))

    def assert_refused(self, run, message):
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertEqual(run.stdout, b"", "no answer")
        stderr = run.stderr.decode()
        self.assertEqual(stderr.count("\n"), 1, f"one stderr line: {stderr!r}")
        self.assertTrue(stderr.startswith("sweep-scope: "), stderr)
        self.assertIn(message, stderr)

    def test_the_git_form_answers_from_the_paths_changed_since_the_merge_base(self):
        self.assert_answer(self.run_reader(self.base, self.docs_head), "not-required")
        self.assert_answer(self.run_reader(self.base, self.lever_head), "required lever")
        self.assert_answer(self.run_reader(self.base, self.mixed_head), "required credential")
        # the base may be a ref, and main moved past the merge base changes nothing for the head
        self.assert_answer(self.run_reader("main", self.lever_head), "required lever")
        self.write(CREDENTIAL, "main moved\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "main moved")
        self.assert_answer(self.run_reader("main", self.docs_head), "not-required")
        self.assert_answer(self.run_reader("main", self.lever_head), "required lever")

    def test_the_git_form_lists_both_paths_of_a_rename(self):
        """A lever file renamed out of its directory still changed a lever path (`--no-renames`)."""
        self.git("switch", "-q", "-c", "renamed", self.base)
        self.git("mv", "scripts/orchestrator/old.py", "docs/old.py")
        self.git("commit", "-q", "-m", "renamed")
        renamed = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        self.assert_answer(self.run_reader(self.base, renamed), "required lever")

    def test_a_failed_git_read_is_exit_2_with_one_line_never_not_required(self):
        """Standing order 21: a head git cannot resolve, a base it cannot resolve, a directory outside a repository,
        and two revisions with no change between them are each exit 2 naming the read, with no answer."""
        self.assert_refused(self.run_reader(self.base, "f" * 40), "git diff --name-only")
        self.assert_refused(self.run_reader("nonexistent-ref", self.docs_head), "git diff --name-only")
        outside = self.root / "outside"
        outside.mkdir()
        self.assert_refused(self.run_reader(self.base, self.docs_head, cwd=outside), "git diff --name-only")
        self.assert_refused(self.run_reader(self.base, self.base), "names no changed path")
        self.assert_refused(self.run_reader(self.base, "-x"), "is not a revision")
        self.assert_refused(self.run_reader("-x", self.docs_head), "usage: sweep-scope.py")

    def test_the_stdin_form_answers_from_the_listing(self):
        """The paths one per line, as `gh pr diff <pr> --name-only` prints them, with or without the last newline."""
        self.assert_answer(self.run_reader("--stdin", stdin=b"docs/plan.md\nREADME.md\n"), "not-required")
        self.assert_answer(self.run_reader("--stdin", stdin=b"docs/plan.md\nREADME.md"), "not-required")
        self.assert_answer(self.run_reader("--stdin", stdin=f"{DOCS[0]}\n{POLICY}\n".encode()), "required policy")
        self.assert_answer(
            self.run_reader("--stdin", stdin=f"{LEVER_PATH}\n{CREDENTIAL}\n".encode()), "required credential"
        )
        self.assert_answer(self.run_reader("--stdin", stdin=f"{DEPLOYED}\n".encode()), "required deployed-executable")
        self.assert_answer(self.run_reader("--stdin", stdin=b"home/dot_agents/agent-config.yaml\n"), "required policy")

    def test_a_listing_that_is_no_listing_of_changed_paths_is_exit_2(self):
        """An empty listing, an empty line, a control character, an absolute path, a `.`, `..` or empty component
        and bytes that are not UTF-8 are each refused naming the shape, never read as `not-required`."""
        for name, listing, message in (
            ("empty", b"", "names no changed path"),
            ("a newline alone", b"\n", "holds an empty line"),
            ("an empty line between", b"docs/a.md\n\nREADME.md\n", "holds an empty line"),
            ("a control character", b"docs/a\x01.md\n", "holds a control character"),
            ("a carriage return", b"docs/a.md\r\n", "holds a control character"),
            ("an absolute path", b"/etc/passwd\n", "is absolute"),
            ("a .. component", b"docs/../scripts/x\n", "holds a '.', '..' or empty component"),
            ("a . component", b"./docs/a.md\n", "holds a '.', '..' or empty component"),
            ("an empty component", b"docs//a.md\n", "holds a '.', '..' or empty component"),
            ("a trailing slash", b"docs/\n", "holds a '.', '..' or empty component"),
            ("not UTF-8", b"docs/\xff.md\n", "not UTF-8"),
        ):
            with self.subTest(name):
                self.assert_refused(self.run_reader("--stdin", stdin=listing), message)

    def test_usage_is_exit_2(self):
        for args in ((), (self.base,), (self.base, self.docs_head, "x"), ("--stdin", "x"), ("--other",)):
            with self.subTest(args=args):
                self.assert_refused(self.run_reader(*args, stdin=b"docs/a.md\n"), "usage: sweep-scope.py")


if __name__ == "__main__":
    unittest.main()
