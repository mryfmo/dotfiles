"""scripts/ci/affected-tests.py (regime-cutover U623): the test modules a change can reach, from a map the selector
builds at run time out of the tree's imports and string literals; `all` for a change to the shared code, the runner,
the selection or the workflow; exit 2 for a read that failed."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELECTOR = ROOT / "scripts/ci/affected-tests.py"

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env  # noqa: E402

# A small repository in the shape of this one: levers and a twin, a library, skills, docs, the files that answer `all`,
# a helper the test modules import, and modules that reach the tree in each of the ways the map reads.
TREE = {
    "scripts/orchestrator/lever.sh": "#!/usr/bin/env bash\necho lever\n",
    "scripts/orchestrator/other.sh": "#!/usr/bin/env bash\necho other\n",
    "home/dot_local/bin/common/executable_lever.sh": "#!/usr/bin/env bash\necho lever\n",
    "scripts/lib/release.sh": "tag() { echo v1; }\n",
    "home/dot_agents/skills/alpha/SKILL.md": "# alpha\n",
    "home/dot_agents/skills/beta/SKILL.md": "# beta\n",
    "home/dot_zshrc": "# zsh\n",
    "docs/page.md": "# page\n",
    "install/common/brew.sh": "brew() { :; }\n",
    "README.md": "# readme\n",
    "Makefile": "unit-test:\n\ttrue\n",
    "pyproject.toml": "[project]\nname = 'x'\n",
    "uv.lock": "version = 1\n",
    ".github/workflows/test.yaml": "name: Unit test\n",
    "scripts/ci/runner.py": "print('runner')\n",
    "tests/unit/helper.py": 'LEVERS = "scripts/orchestrator"\n',
    "tests/unit/fixtures/sample.json": "{}\n",
    # Imports the helper by its bare name, as `discover -s tests/unit` resolves it; names the lever by its file name
    # alone, which is no path, so the lever is reached through the helper's directory literal.
    "tests/unit/test_lever.py": """
        import unittest

        from helper import LEVERS


        class LeverTest(unittest.TestCase):
            def test_runs(self):
                self.assertTrue(LEVERS.endswith("orchestrator"))
                self.assertEqual("lever.sh", "lever.sh")
    """,
    # The dotted import `python -m unittest` resolves from the repository root.
    "tests/unit/test_dotted.py": """
        import unittest

        from tests.unit.helper import LEVERS


        class DottedTest(unittest.TestCase):
            def test_levers(self):
                self.assertTrue(LEVERS)
    """,
    # An f-string: the directory before its first field reaches every skill.
    "tests/unit/test_skills.py": """
        import unittest


        def page(skill):
            return f"home/dot_agents/skills/{skill}/SKILL.md"


        class SkillsTest(unittest.TestCase):
            def test_page(self):
                self.assertIn("alpha", page("alpha"))
    """,
    # A path inside the prose of a docstring, and a root file by its bare name.
    "tests/unit/test_docs.py": '''
        """Reads the page docs/page.md (a path inside prose counts; the word README.md here does not)."""

        import unittest

        README = "README.md"


        class DocsTest(unittest.TestCase):
            def test_page(self):
                pass
    ''',
    # A path inside a longer command string.
    "tests/unit/test_release.py": """
        import unittest

        COMMAND = "bash -c 'source scripts/lib/release.sh && tag'"


        class ReleaseTest(unittest.TestCase):
            def test_command(self):
                self.assertIn("tag", COMMAND)
    """,
    # A glob: the directory before it.
    "tests/unit/test_glob.py": """
        import unittest

        PATTERN = "install/**/*.sh"


        class GlobTest(unittest.TestCase):
            def test_pattern(self):
                self.assertIn("*", PATTERN)
    """,
    # Bare words that are also top-level directories, and a path that is not in the tree: none of them reaches.
    "tests/unit/test_words.py": """
        import json
        import unittest

        WORDS = ("home", "scripts", "tests", "docs")
        MISSING = "install/common/missing.sh"


        class WordsTest(unittest.TestCase):
            def test_words(self):
                self.assertEqual(4, len(json.loads(json.dumps(WORDS))))
    """,
}


def load_selector():
    """The selector as a module, for its `select` and `Mapper` over a tree without a diff."""
    spec = importlib.util.spec_from_file_location("affected_tests", SELECTOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def isolated_env() -> dict[str, str]:
    return quiet_git_env({**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"})


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
        env=isolated_env(),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def write(repo: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(text).lstrip("\n") if name.endswith(".py") else text)


def scratch_repository(temp: Path) -> tuple[Path, str]:
    """A repository holding TREE at its first commit on main; returns (repo, base sha)."""
    repo = git_init(temp / "repo", "-b", "main", env=isolated_env())
    write(repo, TREE)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    return repo, git(repo, "rev-parse", "HEAD")


def head_with(repo: Path, base: str, branch: str, writes: dict[str, str] | None = None, removes=()) -> str:
    """A commit on `branch` from `base` that writes and removes the given paths; the working tree is that head."""
    git(repo, "checkout", "-q", "-B", branch, base)
    write(repo, writes or {})
    for name in removes:
        git(repo, "rm", "-q", name)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--allow-empty", "-m", branch)
    return git(repo, "rev-parse", "HEAD")


def selector(repo: Path, base: str, head: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", str(SELECTOR), "--base", base, "--head", head, *args],
        cwd=repo,
        env=isolated_env(),
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )


class SelectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.holder = tempfile.TemporaryDirectory()
        cls.repo, cls.base = scratch_repository(Path(cls.holder.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.holder.cleanup()

    def selected(self, head: str) -> list[str]:
        result = selector(self.repo, self.base, head, "--explain")
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout.splitlines()

    def test_a_lever_change_selects_the_tests_that_reach_its_directory_through_an_import(self) -> None:
        # The map reaches a lever's test from the lever's path: test_lever imports the helper, whose literal names the
        # levers' directory; test_dotted imports the same helper through the dotted form.
        head = head_with(self.repo, self.base, "lever", {"scripts/orchestrator/lever.sh": "echo changed\n"})
        result = selector(self.repo, self.base, head, "--explain")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["tests/unit/test_dotted.py", "tests/unit/test_lever.py"], result.stdout.splitlines())
        self.assertIn("affected-tests: 1 changed paths from", result.stderr)
        self.assertIn(
            "affected-tests: tests/unit/test_lever.py: scripts/orchestrator/lever.sh is scripts/orchestrator/, "
            "named as `scripts/orchestrator` in tests/unit/helper.py (imported)\n",
            result.stderr,
        )
        self.assertIn("affected-tests: 2 of 7 modules selected\n", result.stderr)
        # Without --explain, stdout is the same list and stderr is silent.
        quiet = selector(self.repo, self.base, head)
        self.assertEqual((0, result.stdout, ""), (quiet.returncode, quiet.stdout, quiet.stderr))

    def test_the_twin_of_a_lever_selects_the_levers_tests(self) -> None:
        # And from its twin's path: the deployed copy under home/dot_local/bin/common counts as the lever.
        head = head_with(
            self.repo, self.base, "twin", {"home/dot_local/bin/common/executable_lever.sh": "echo changed\n"}
        )
        result = selector(self.repo, self.base, head, "--explain")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["tests/unit/test_dotted.py", "tests/unit/test_lever.py"], result.stdout.splitlines())
        self.assertIn(
            "scripts/orchestrator/lever.sh (the twin of home/dot_local/bin/common/executable_lever.sh) is "
            "scripts/orchestrator/,",
            result.stderr,
        )

    def test_a_helper_a_fixture_or_an_init_under_the_start_directory_answers_all(self) -> None:
        for name, writes in (
            ("helper", {"tests/unit/helper.py": 'LEVERS = "scripts/orchestrator/"\n'}),
            ("fixture", {"tests/unit/fixtures/sample.json": '{"x": 1}\n'}),
            ("package-init", {"tests/unit/__init__.py": ""}),
            # Together with a mapped change, still `all`: the shared code may change what every module does.
            ("helper-and-lever", {"tests/unit/helper.py": "X = 1\n", "scripts/orchestrator/lever.sh": "x\n"}),
        ):
            with self.subTest(case=name):
                head = head_with(self.repo, self.base, f"shared-{name}", writes)
                result = selector(self.repo, self.base, head, "--explain")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("all\n", result.stdout)
                self.assertIn("is under tests/unit/ and no test module: shared code", result.stderr)
                self.assertIn("affected-tests: all modules selected\n", result.stderr)

    def test_the_workflow_the_runner_the_makefile_and_the_environment_files_answer_all(self) -> None:
        for name, reason in (
            (".github/workflows/test.yaml", ".github/workflows/test.yaml is under .github/"),
            ("scripts/ci/runner.py", "scripts/ci/runner.py is under scripts/"),
            ("scripts/ci/affected-tests.py", "scripts/ci/affected-tests.py is under scripts/"),
            ("Makefile", "Makefile builds the environment every module runs in"),
            ("pyproject.toml", "pyproject.toml builds the environment every module runs in"),
            ("uv.lock", "uv.lock builds the environment every module runs in"),
        ):
            with self.subTest(path=name):
                head = head_with(self.repo, self.base, f"all-{len(reason)}", {name: "changed\n"})
                result = selector(self.repo, self.base, head, "--explain")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("all\n", result.stdout)
                self.assertIn(f"affected-tests: all: {reason}\n", result.stderr)

    def test_a_changed_test_module_selects_itself(self) -> None:
        head = head_with(
            self.repo, self.base, "module", {"tests/unit/test_words.py": TREE["tests/unit/test_words.py"] + "\n"}
        )
        result = selector(self.repo, self.base, head, "--explain")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["tests/unit/test_words.py"], result.stdout.splitlines())
        self.assertIn("tests/unit/test_words.py: tests/unit/test_words.py is the module itself\n", result.stderr)
        # A new module selects itself too, and a changed helper module that others import selects them.
        added = head_with(self.repo, self.base, "added", {"tests/unit/test_new.py": "import unittest\n"})
        self.assertEqual(["tests/unit/test_new.py"], self.selected(added))

    def test_a_directory_prefix_from_an_f_string_or_a_glob_reaches_everything_under_it(self) -> None:
        skill = head_with(self.repo, self.base, "skill", {"home/dot_agents/skills/beta/SKILL.md": "# beta 2\n"})
        self.assertEqual(["tests/unit/test_skills.py"], self.selected(skill))
        new_skill = head_with(self.repo, self.base, "new-skill", {"home/dot_agents/skills/gamma/SKILL.md": "# g\n"})
        self.assertEqual(["tests/unit/test_skills.py"], self.selected(new_skill))
        installer = head_with(self.repo, self.base, "installer", {"install/common/brew.sh": "brew() { echo; }\n"})
        self.assertEqual(["tests/unit/test_glob.py"], self.selected(installer))

    def test_a_path_inside_a_longer_literal_and_a_root_file_by_its_name_are_reached(self) -> None:
        page = head_with(self.repo, self.base, "page", {"docs/page.md": "# page 2\n"})
        self.assertEqual(["tests/unit/test_docs.py"], self.selected(page))
        readme = head_with(self.repo, self.base, "readme", {"README.md": "# readme 2\n"})
        self.assertEqual(["tests/unit/test_docs.py"], self.selected(readme))
        library = head_with(self.repo, self.base, "library", {"scripts/lib/release.sh": "tag() { echo v2; }\n"})
        self.assertEqual(["tests/unit/test_release.py"], self.selected(library))

    def test_a_bare_word_never_reaches_a_directory_and_an_unreached_change_selects_nothing(self) -> None:
        # test_words spells "home", "scripts", "tests" and "docs" as whole literals: words, not prefixes, so a change
        # under home/ that no module names reaches nothing, and the answer is empty with exit 0.
        head = head_with(self.repo, self.base, "zshrc", {"home/dot_zshrc": "# zsh 2\n"})
        result = selector(self.repo, self.base, head, "--explain")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)
        self.assertIn("affected-tests: nothing: home/dot_zshrc reaches no module\n", result.stderr)
        self.assertIn("affected-tests: 0 of 7 modules selected\n", result.stderr)
        # Another lever: reached through the directory literal, never through the word "scripts".
        other = head_with(self.repo, self.base, "other", {"scripts/orchestrator/other.sh": "echo other 2\n"})
        self.assertEqual(["tests/unit/test_dotted.py", "tests/unit/test_lever.py"], self.selected(other))

    def test_a_deleted_lever_and_a_renamed_lever_select_its_tests(self) -> None:
        deleted = head_with(self.repo, self.base, "deleted", removes=["scripts/orchestrator/lever.sh"])
        self.assertEqual(["tests/unit/test_dotted.py", "tests/unit/test_lever.py"], self.selected(deleted))
        # --no-renames lists both sides: the old lever path still selects its tests.
        git(self.repo, "checkout", "-q", "-B", "renamed", self.base)
        git(self.repo, "mv", "scripts/orchestrator/lever.sh", "home/moved.sh")
        git(self.repo, "commit", "-q", "-m", "renamed")
        renamed = git(self.repo, "rev-parse", "HEAD")
        self.assertEqual(["tests/unit/test_dotted.py", "tests/unit/test_lever.py"], self.selected(renamed))

    def test_a_diff_that_fails_is_exit_2_with_nothing_on_stdout(self) -> None:
        result = selector(self.repo, self.base, "0" * 40)
        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertIn(f"affected-tests: git diff {self.base}...{'0' * 40} failed with exit 128", result.stderr)

    def test_a_module_that_cannot_be_parsed_or_a_missing_start_directory_is_exit_2(self) -> None:
        broken = head_with(self.repo, self.base, "broken", {"tests/unit/test_broken.py": "def (:\n"})
        result = selector(self.repo, self.base, broken)
        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertIn("affected-tests: cannot parse tests/unit/test_broken.py:", result.stderr)
        head = head_with(self.repo, self.base, "start", {"scripts/orchestrator/lever.sh": "x\n"})
        result = selector(self.repo, self.base, head, "--start", "tests/none")
        self.assertEqual(2, result.returncode)
        self.assertIn("is not a directory", result.stderr)
        self.assertEqual("", result.stdout)


class NormaliseTest(unittest.TestCase):
    """The literal reader, case by case: what is a path candidate and of which kind."""

    def test_the_forms_a_literal_takes(self) -> None:
        module = load_selector()
        cases = {
            ("scripts/orchestrator/pr-merge.sh", False): ("scripts/orchestrator/pr-merge.sh", "any"),
            ("home/dot_agents/skills", False): ("home/dot_agents/skills", "any"),
            ("docs/", False): ("docs", "dir"),
            ("Makefile", False): ("Makefile", "file"),
            ("home", False): ("home", "file"),
            ("./scripts/x.sh", False): ("scripts/x.sh", "any"),
            ("home/dot_local/bin/common/executable_*", False): ("home/dot_local/bin/common", "dir"),
            ("home/dot_agents/skills/{", False): ("home/dot_agents/skills", "dir"),
            ("install/**/*.sh", False): ("install", "dir"),
            ("*.md", False): None,
            ("test_*.py", False): None,
            ('scripts/apply-check.sh --system "${SYSTEM}"', False): None,
            ("/usr/bin/python3", False): None,
            ("~/.local/bin/x", False): None,
            ("${HOME}/.config", False): None,
            ("--base", False): None,
            ("https://github.com/x/y", False): None,
            ("../outside", False): None,
            ("a//b", False): None,
            (".", False): None,
            ("", False): None,
            # A token inside a longer literal needs a slash; punctuation around it is prose.
            ("home", True): None,
            ("(scripts/orchestrator/pr-merge.sh)", True): ("scripts/orchestrator/pr-merge.sh", "any"),
            ("`docs/`,", True): ("docs", "dir"),
            ("scripts/old.sh\tR1\t{", False): None,
        }
        for (text, token), expected in cases.items():
            with self.subTest(text=text, token=token):
                self.assertEqual(expected, module.normalise(text, token))

    def test_the_twin_rule_pairs_a_lever_with_its_deployed_copy(self) -> None:
        module = load_selector()
        self.assertEqual(
            "home/dot_local/bin/common/executable_pr-merge.sh", module.twin("scripts/orchestrator/pr-merge.sh")
        )
        self.assertEqual(
            "scripts/orchestrator/pr-merge.sh", module.twin("home/dot_local/bin/common/executable_pr-merge.sh")
        )
        for other in ("scripts/orchestrator/sub/x.sh", "home/dot_local/bin/common/README.md", "scripts/x.sh"):
            with self.subTest(path=other):
                self.assertIsNone(module.twin(other))
        self.assertEqual(["a/", "a/b/"], module.ancestors("a/b/c"))


class RealTreeTest(unittest.TestCase):
    """The map over this repository: the brief's cases, read from the real modules."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_selector()
        cls.modules = cls.module.test_modules(ROOT, ROOT / "tests/unit", "test*.py")

    def select(self, *changed: str) -> tuple[list[str], dict[str, list[str]]]:
        return self.module.select(ROOT, Path("tests/unit"), "test*.py", list(changed))

    def test_a_lever_and_its_twin_reach_the_levers_test_and_fewer_than_every_module(self) -> None:
        for changed in ("scripts/orchestrator/pr-merge.sh", "home/dot_local/bin/common/executable_pr-merge.sh"):
            with self.subTest(changed=changed):
                selected, reasons = self.select(changed)
                self.assertIn("tests/unit/test_pr_merge.py", selected)
                self.assertIn("tests/unit/test_pr_levers.py", selected)
                self.assertIn("tests/unit/test_ci_workflows.py", selected)
                self.assertLess(len(selected), len(self.modules) // 2, selected)
                self.assertTrue(all(reasons[module] for module in selected))

    def test_the_shared_code_the_runner_the_workflow_and_the_makefile_answer_all(self) -> None:
        for changed in (
            "tests/unit/scratch_git.py",
            "tests/unit/agent_home_isolation.py",
            "scripts/ci/unittest-shards.py",
            "scripts/ci/affected-tests.py",
            ".github/workflows/test.yaml",
            "Makefile",
            "uv.lock",
        ):
            with self.subTest(changed=changed):
                selected, reasons = self.select(changed)
                self.assertEqual(["all"], selected)
                self.assertEqual(["all"], list(reasons))

    def test_a_test_module_selects_itself_and_the_modules_that_import_it(self) -> None:
        selected, reasons = self.select("tests/unit/test_pr_levers.py")
        self.assertIn("tests/unit/test_pr_levers.py", selected)
        self.assertIn("tests/unit/test_pr_merge.py", selected)
        self.assertIn("tests/unit/test_pr_levers.py is the module itself", reasons["tests/unit/test_pr_levers.py"])
        self.assertIn(
            "tests/unit/test_pr_levers.py is tests/unit/test_pr_levers.py, imported by tests/unit/test_pr_merge.py",
            reasons["tests/unit/test_pr_merge.py"],
        )
        selected, _ = self.select("tests/unit/test_affected_tests.py")
        self.assertIn("tests/unit/test_affected_tests.py", selected)

    def test_the_imports_resolve_as_discover_and_python_m_unittest_resolve_them(self) -> None:
        mapper = self.module.Mapper(ROOT, set())
        for module, imported in (
            ("tests/unit/test_ci_workflows.py", "tests/unit/workflow_lock.py"),
            ("tests/unit/test_ci_workflows.py", "tests/unit/agent_home_isolation.py"),
            ("tests/unit/test_pr_merge.py", "tests/unit/test_pr_levers.py"),
            ("tests/unit/test_validate_agent_assets.py", "tests/unit/test_generate_agent_configs.py"),
            ("tests/unit/test_affected_tests.py", "tests/unit/scratch_git.py"),
        ):
            with self.subTest(module=module, imported=imported):
                self.assertIn(imported, mapper.imports(module))
        # The standard library and third-party modules are no repository paths.
        self.assertFalse([name for name in mapper.imports("tests/unit/test_affected_tests.py") if "unittest" in name])

    def test_every_module_of_the_tree_is_mapped_and_reaches_a_path(self) -> None:
        # The map covers the suite: each module parses, and each reaches at least one path of the tree, so a change
        # to that path selects it (a module reaching nothing could never be selected by anything but itself).
        self.assertGreater(len(self.modules), 100)
        mapper = self.module.Mapper(ROOT, set())
        for module in self.modules:
            with self.subTest(module=module):
                self.assertTrue(mapper.reach(module), module)


if __name__ == "__main__":
    unittest.main()
