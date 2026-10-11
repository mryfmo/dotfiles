import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "scripts/main-tests.sh"
WORKFLOW = ROOT / ".github/workflows/test.yaml"
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

    def harness(self, pr: dict[str, str], deleted=(), main=None, env=None) -> subprocess.CompletedProcess:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        self.git(root, "init", "-q", "-b", "main")
        for files, message in ((main or MAIN, "main"), (pr, "pr")):
            for path, text in files.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_text(text)
                if "/bin/" in path:  # a planted interpreter
                    (root / path).chmod(0o755)
            if message == "pr":
                self.git(root, "switch", "-q", "-c", "pr")
                for path in deleted:
                    (root / path).unlink()
            self.git(root, "add", "-A")
            self.git(root, "commit", "-q", "--allow-empty", "-m", message)
        return subprocess.run(
            ["bash", str(HARNESS), "main"],
            cwd=root,
            env={**GIT_ENV, **(env or {})},
            capture_output=True,
            text=True,
            check=False,
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
        self.assertIn("test_contract (test_foo.FooTest.test_contract) ... ok", kept.stdout + kept.stderr)

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
                self.assertIn("test_contract (test_foo.FooTest.test_contract) ... ok", result.stdout + result.stderr)

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

    def test_a_helper_failure_fails_the_run(self) -> None:
        # uv cannot fetch PyYAML from a dead index; that must not read as "no script change".
        result = self.harness({"install/x.sh": "changed\n"}, env={"UV_INDEX_URL": "http://127.0.0.1:9/simple"})
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("main-tests: no script change", result.stdout)

    def test_nothing_from_the_pr_runs_before_mains_harness(self) -> None:
        text = WORKFLOW.read_text()
        job = text[text.index("\n  main-tests:\n") :]
        job = job[: job.index("\n  test:\n")]
        commands = [line.strip() for line in job.splitlines() if not line.strip().startswith("#")]
        for line in commands:
            for target in re.findall(r"(?:^|&&|;|\|)\s*(?:source|\.|bash|sh)\s+(\S+)", line):
                with self.subTest(line=line):
                    self.assertTrue(target.strip('"').startswith("${RUNNER_TEMP}/"), line)
        self.assertIn(
            'git show origin/main:scripts/lib/github-release.sh > "${RUNNER_TEMP}/scripts/lib/github-release.sh"', job
        )
        self.assertLess(job.index("git fetch --no-tags origin main"), job.index("source "))
        # Only the harness pair may fall back to the PR's copy.
        self.assertEqual(1, job.count('cp "${path}"'))
        self.assertIn("for path in scripts/main-tests.sh scripts/lib/contract_markers.py; do", job)

    def test_a_planted_venv_is_not_used(self) -> None:
        marker = Path(tempfile.mkdtemp()) / "planted-python-ran"
        self.addCleanup(shutil.rmtree, marker.parent)
        planted = f"#!/bin/sh\ntouch {marker}\nexit 0\n"
        pr = {".venv/bin/python": planted, ".venv/bin/python3": planted, ".venv/pyvenv.cfg": "version = 3.12.0\n"}
        result = self.harness({"install/x.sh": "changed\n", **pr})
        self.assertPasses(result)
        self.assertFalse(marker.exists(), "uv ran the PR's .venv interpreter")

    def test_a_zero_exit_without_a_summary_fails(self) -> None:
        loads = "import runpy\nfrom pathlib import Path\n\nrunpy.run_path(str(Path(__file__).resolve().parents[2] / 'scripts/baz.py'))\n"
        main = {**MAIN, "scripts/baz.py": "VALUE = 1\n", "tests/unit/test_baz.py": loads}
        result = self.harness({"scripts/baz.py": "import os\n\nos._exit(0)\n"}, main=main)
        self.assertFails(result, "main-tests: no complete unittest run (no result file)")

    def test_a_forged_summary_without_the_runner_nonce_fails(self) -> None:
        loads = "import runpy\nfrom pathlib import Path\n\nrunpy.run_path(str(Path(__file__).resolve().parents[2] / 'scripts/baz.py'))\n"
        main = {**MAIN, "scripts/baz.py": "VALUE = 1\n", "tests/unit/test_baz.py": loads}
        summary = "import json\nimport os\nimport sys\n\nsys.stderr.write('Ran 3 tests in 0.010s\\n\\nOK\\n')\n"
        write = "json.dump({'nonce': nonce, 'ran': 3, 'failures': 0, 'errors': 0}, open(sys.argv[2], 'w'))\n"
        steal = "try:\n    nonce = os.read(3, 64).decode().strip()\nexcept OSError:\n    nonce = 'unreadable'\n"
        for forger, reason in (
            (summary, "no result file"),
            (summary + "nonce = 'forged'\n" + write, "the result does not carry this run's nonce"),
            (summary + steal + write, "the result does not carry this run's nonce"),
        ):
            with self.subTest(reason=reason, steals="os.read(3" in forger):
                result = self.harness({"scripts/baz.py": forger + "os._exit(0)\n"}, main=main)
                self.assertFails(result, f"main-tests: no complete unittest run ({reason})")
        # An atexit hook that rewrites the genuine result (nonce and all) must never run: the runner leaves by os._exit.
        rewrite = (
            "import atexit\nimport json\nimport os\nimport sys\n\n\ndef forge():\n    record = json.load(open(sys.argv[2]))\n"
            "    record.update(failures=0, errors=0)\n    json.dump(record, open(sys.argv[2], 'w'))\n    os._exit(0)\n\n\n"
            "atexit.register(forge)\n"
        )
        result = self.harness({"scripts/baz.py": rewrite, "scripts/foo.sh": "changed contract\n"}, main=main)
        self.assertFails(result, "FAIL: test_ordinary (test_foo.FooTest")

    def test_a_short_contract_summary_fails(self) -> None:
        # Two contracts selected; the PR's script prints a one-test summary and exits 0 at import.
        body = "\n    @contract\n    def test_{n}(self):\n        pass\n"
        qux = (
            "import runpy\nimport unittest\nfrom pathlib import Path\n\nfrom regime_contract import contract\n\n"
            "runpy.run_path(str(Path(__file__).resolve().parents[2] / 'scripts/qux.py'))\n\n\n"
            "class QuxTest(unittest.TestCase):" + body.format(n="a") + body.format(n="b")
        )
        main = {**MAIN, "scripts/qux.py": "VALUE = 1\n", "tests/unit/test_qux.py": qux}
        forged = "import os\nimport sys\n\nsys.stderr.write('Ran 1 test in 0.001s\\n\\nOK\\n')\nos._exit(0)\n"
        files = ["scripts/qux.py", "tests/unit/test_qux.py"]
        pr = {"scripts/qux.py": forged, "tests/unit/test_qux.py": qux.replace("    @contract\n", ""), **task(files)}
        self.assertFails(self.harness(pr, main=main), "main-tests: no complete unittest run (no result file)")

    def test_a_declared_module_without_its_script_stays_undeclared(self) -> None:
        pr = {
            "scripts/foo.sh": "changed contract\n",
            "tests/unit/test_foo.py": PROMOTED,
            **task(["tests/unit/test_foo.py"]),
        }
        self.assertFails(self.harness(pr), "FAIL: test_ordinary (test_foo.FooTest")

    def test_a_renamed_script_still_triggers(self) -> None:
        result = self.harness({"elsewhere/foo.sh": "ordinary contract\n"}, deleted=["scripts/foo.sh"])
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("main-tests: no script change", result.stdout)

    def test_an_empty_contract_class_is_no_contract(self) -> None:
        empty = BAR + "\n\n@contract\nclass Pact(unittest.TestCase):\n    def helper(self):\n        pass\n"
        main = {
            **MAIN,
            "tests/unit/test_bar.py": empty.replace(
                "import unittest\n", "import unittest\n\nfrom regime_contract import contract\n", 1
            ),
        }
        pr = {
            "scripts/bar.sh": "changed\n",
            "tests/unit/test_bar.py": BAR,
            **task(["scripts/bar.sh", "tests/unit/test_bar.py"]),
        }
        self.assertFails(self.harness(pr, main=main), "main-tests: no contract on main for tests/unit/test_bar.py")

    def test_no_script_change_skips(self) -> None:
        result = self.harness({"README.md": "changed\n", "tests/unit/test_bar.py": "broken"})
        self.assertPasses(result)
        self.assertEqual("main-tests: no script change\n", result.stdout)

    def test_an_install_change_triggers_the_run(self) -> None:
        result = self.harness({"install/x.sh": "changed\n"})
        self.assertPasses(result)
        self.assertIn("main-tests: undeclared mode, main's modules as they are: test_bar test_foo", result.stdout)
        self.assertIn("Ran 3 tests", result.stdout + result.stderr)

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
        self.assertIn("test_contract (test_foo.FooTest.test_contract) ... ok", deleted.stdout + deleted.stderr)

    def test_more_than_one_task_file_fails(self) -> None:
        pr = {"scripts/foo.sh": "ordinary contract 2\n", **task([]), **task([], task_id="dotfiles-T998-other-a01")}
        self.assertFails(self.harness(pr), "main-tests: more than one task.md in the range")


if __name__ == "__main__":
    unittest.main()
