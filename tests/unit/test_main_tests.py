import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "scripts/main-tests.sh"
GIT_ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}

# Scratch modules resolve ROOT from their own path, as the real ones do. Decorators stay in
# strings: main-tests also reads this module's own decorators.
FOO = """import unittest
from pathlib import Path

{imports}

ROOT = Path(__file__).resolve().parents[2]


class FooTest(unittest.TestCase):
    def test_ordinary(self):
        self.assertEqual("ordinary", (ROOT / "scripts/foo.sh").read_text().split()[0])

    {decorator}
    def test_contract(self):
        self.assertIn("contract", (ROOT / "scripts/foo.sh").read_text())
"""
DORMANT = FOO.format(imports="from regime_contract import contract", decorator="@contract")
PROMOTED = FOO.format(imports="", decorator="")
BAR = """import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class BarTest(unittest.TestCase):
    def test_ordinary(self):
        self.assertEqual("bar\\n", (ROOT / "scripts/bar.sh").read_text())
"""
MAIN = {
    "README.md": "readme\n",
    "install/x.sh": "x\n",
    "scripts/foo.sh": "ordinary contract\n",
    "scripts/bar.sh": "bar\n",
    "scripts/legacy-task-ids.txt": "t1\n",
    "tests/unit/regime_contract.py": (ROOT / "tests/unit/regime_contract.py").read_text(),
    "tests/unit/test_foo.py": DORMANT,
    "tests/unit/test_bar.py": BAR,
}
FOO_FILES = ("scripts/foo.sh", "tests/unit/test_foo.py")


def task(files, task_id="dotfiles-T999-demo-a01", tier=None) -> dict[str, str]:
    lines = ["---", f"task_id: {task_id}", *([f"tier: {tier}"] if tier else []), "allowed_files:"]
    lines += [f"  - {path}" for path in files] + ["---", "", "# demo", ""]
    return {f".orchestration/{task_id}/task.md": "\n".join(lines)}


class MainTestsHarnessTest(unittest.TestCase):
    def git(self, root: Path, *args: str) -> None:
        identity = ("-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false")
        subprocess.run(["git", *identity, *args], cwd=root, env=GIT_ENV, check=True, capture_output=True)

    def harness(self, pr: dict[str, str], deleted=(), main=None) -> subprocess.CompletedProcess:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        self.git(root, "init", "-q", "-b", "main")
        for files, message in ((main or MAIN, "main"), (pr, "pr")):
            for path, text in files.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_text(text)
            if message == "pr":
                self.git(root, "switch", "-q", "-c", "pr")
                for path in deleted:
                    (root / path).unlink()
            self.git(root, "add", "-A")
            self.git(root, "commit", "-q", "--allow-empty", "-m", message)
        return subprocess.run(
            ["bash", str(HARNESS), "main"], cwd=root, env=GIT_ENV, capture_output=True, text=True, check=False
        )

    def assertFails(self, result, message: str) -> None:
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(message, result.stdout + result.stderr)

    def assertPasses(self, result) -> None:
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_an_undeclared_script_change_meets_mains_ordinary_tests(self) -> None:
        for pr in ({}, task(["scripts/bar.sh", "tests/unit/test_bar.py"], tier="review")):
            with self.subTest(task=bool(pr)):
                result = self.harness({"scripts/foo.sh": "changed contract\n", **pr})
                self.assertFails(result, "FAIL: test_ordinary (test_foo.FooTest")

    def test_a_declared_script_meets_mains_contract_only(self) -> None:
        broken = self.harness({"scripts/foo.sh": "changed\n", "tests/unit/test_foo.py": PROMOTED, **task(FOO_FILES)})
        self.assertFails(broken, "FAIL: test_contract (test_foo.FooTest")
        self.assertNotIn("test_foo.FooTest.test_ordinary", broken.stdout + broken.stderr)
        kept = self.harness(
            {"scripts/foo.sh": "changed contract\n", "tests/unit/test_foo.py": PROMOTED, **task(FOO_FILES)}
        )
        self.assertPasses(kept)
        self.assertIn("test_contract (test_foo.FooTest.test_contract) ... ok", kept.stderr)

    def test_a_design_tier_module_needs_a_contract_on_main(self) -> None:
        bar = {"scripts/bar.sh": "changed\n"}
        for tier in ("design", None):
            with self.subTest(tier=tier):
                result = self.harness({**bar, **task(["scripts/bar.sh", "tests/unit/test_bar.py"], tier=tier)})
                self.assertFails(result, "main-tests: no contract on main for tests/unit/test_bar.py")
        self.assertPasses(self.harness({**bar, **task(["scripts/bar.sh", "tests/unit/test_bar.py"], tier="review")}))

    def test_an_implementation_must_promote_its_contracts(self) -> None:
        foo = {"scripts/foo.sh": "changed contract\n"}
        dormant = self.harness({**foo, "tests/unit/test_foo.py": DORMANT + "\n", **task(FOO_FILES)})
        self.assertFails(dormant, "main-tests: contract still dormant in tests/unit/test_foo.py")
        self.assertPasses(self.harness({**foo, **task(FOO_FILES, task_id="dotfiles-T999-demo-contract-a01")}))

    def test_aliased_and_inline_contracts_are_still_dormant(self) -> None:
        inline = "@unittest.skipUnless(os.environ.get('REGIME_CONTRACT') == '1', 'dormant contract')"
        for imports, decorator in (
            ("import regime_contract as rc", "@rc.contract"),
            ("from regime_contract import contract as c", "@c"),
            ("import os", inline),
        ):
            with self.subTest(decorator=decorator):
                module = FOO.format(imports=imports, decorator=decorator)
                main = {**MAIN, "tests/unit/test_foo.py": module}
                pr = {
                    "scripts/foo.sh": "changed contract\n",
                    "tests/unit/test_foo.py": module + "\n",
                    **task(FOO_FILES),
                }
                result = self.harness(pr, main=main)
                self.assertFails(result, "main-tests: contract still dormant in tests/unit/test_foo.py")
                self.assertIn("test_contract (test_foo.FooTest.test_contract) ... ok", result.stderr)

    def test_a_deleted_module_still_runs_from_main(self) -> None:
        result = self.harness({"scripts/foo.sh": "changed contract\n"}, deleted=["tests/unit/test_foo.py"])
        self.assertFails(result, "FAIL: test_ordinary (test_foo.FooTest")

    def test_files_the_pr_plants_cannot_replace_mains_runner(self) -> None:
        for path in ("tests/unit/unittest.py", "unittest.py"):
            with self.subTest(path=path):
                result = self.harness({"scripts/foo.sh": "changed contract\n", path: "raise SystemExit(0)\n"})
                self.assertFails(result, "FAIL: test_ordinary (test_foo.FooTest")

    def test_a_uv_config_the_pr_plants_is_ignored(self) -> None:
        # Honoured, this index would make uv fail to fetch PyYAML.
        result = self.harness({"install/x.sh": "changed\n", "uv.toml": 'index-url = "http://127.0.0.1:9/simple"\n'})
        self.assertPasses(result)

    def test_no_script_change_skips(self) -> None:
        result = self.harness({"README.md": "changed\n", "tests/unit/test_bar.py": "broken"})
        self.assertPasses(result)
        self.assertEqual("main-tests: no script change\n", result.stdout)

    def test_an_install_change_triggers_the_run(self) -> None:
        result = self.harness({"install/x.sh": "changed\n"})
        self.assertPasses(result)
        self.assertIn("main-tests: undeclared mode, main's modules as they are: test_bar test_foo", result.stdout)
        self.assertIn("Ran 3 tests", result.stderr)

    def test_design_scripts_need_declared_modules_that_exist(self) -> None:
        # Promoted and passing otherwise, so the uncovered script is the only failure.
        files = ["scripts/foo.sh", "scripts/baz.sh", "tests/unit/test_foo.py"]
        uncovered = self.harness({"scripts/baz.sh": "baz\n", "tests/unit/test_foo.py": PROMOTED, **task(files)})
        self.assertFails(
            uncovered, "main-tests: design script scripts/baz.sh has no declared contract module tests/unit/test_baz.py"
        )
        self.assertNotIn("contract still dormant", uncovered.stdout)
        self.assertPasses(
            self.harness({"scripts/legacy-task-ids.txt": "t2\n", **task(["scripts/legacy-task-ids.txt"])})
        )
        deleted = self.harness(
            {"scripts/foo.sh": "changed contract\n", **task(FOO_FILES)}, deleted=["tests/unit/test_foo.py"]
        )
        self.assertFails(deleted, "main-tests: declared module tests/unit/test_foo.py deleted")
        self.assertIn("test_contract (test_foo.FooTest.test_contract) ... ok", deleted.stderr)

    def test_more_than_one_task_file_fails(self) -> None:
        pr = {"scripts/foo.sh": "ordinary contract 2\n", **task([]), **task([], task_id="dotfiles-T998-other-a01")}
        self.assertFails(self.harness(pr), "main-tests: more than one task.md in the range")


if __name__ == "__main__":
    unittest.main()
