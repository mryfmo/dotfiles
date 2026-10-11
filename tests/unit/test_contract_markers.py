import importlib.util
import io
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts/lib/contract_markers.py"
SPEC = importlib.util.spec_from_file_location("contract_markers", HELPER)
markers = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(markers)

# Decorator samples stay strings: main-tests reads this module's own decorators too.
BODY = """
class FooTest(unittest.TestCase):
    def test_ordinary(self):
        pass

    {decorator}
    def test_contract(self):
        pass
"""
FORMS = {
    "decorated": ("from regime_contract import contract", "@contract"),
    "from-alias": ("from regime_contract import contract as c", "@c"),
    "module-alias": ("import regime_contract as rc", "@rc.contract"),
    "module": ("import regime_contract", "@regime_contract.contract"),
    "inline": ("import os", "@unittest.skipUnless(os.environ.get('REGIME_CONTRACT') == '1', 'dormant contract')"),
    "inline-bare": ("from unittest import skipUnless", '@skipUnless(os.environ.get("REGIME_CONTRACT") == "1", "x")'),
}


class ContractMarkersTest(unittest.TestCase):
    def write(self, text: str, name: str = "test_foo.py") -> str:
        directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, directory)
        path = Path(directory, name)
        path.write_text(text)
        return str(path)

    def module(self, form: str) -> str:
        imports, decorator = FORMS[form]
        return self.write(f"import unittest\n{imports}\n" + BODY.format(decorator=decorator))

    def test_every_form_is_found_on_its_method(self) -> None:
        for form in FORMS:
            with self.subTest(form=form):
                path = self.module(form)
                self.assertEqual(["test_foo.FooTest.test_contract"], markers.contracts(path))
                self.assertEqual(1, markers.main(["dormant", path]))

    def test_undecorated_and_unrelated_decorators_are_not_contracts(self) -> None:
        for decorator in ("", "@unittest.skip('later')", "@contract", "@unittest.skipUnless(True, 'x')"):
            with self.subTest(decorator=decorator):
                # No regime_contract import: a local name `contract` is not the regime's decorator.
                path = self.write("import unittest\n" + BODY.format(decorator=decorator))
                self.assertEqual([], markers.contracts(path))
                self.assertEqual(0, markers.main(["dormant", path]))

    def test_a_decorated_class_is_one_id(self) -> None:
        path = self.write(
            "import unittest\nfrom regime_contract import contract\n\n\n@contract\nclass Pact(unittest.TestCase):\n"
            "    def test_a(self):\n        pass\n"
        )
        self.assertEqual(["test_foo.Pact"], markers.contracts(path))

    def test_a_nested_contract_still_counts_as_dormant(self) -> None:
        path = self.write(
            "from regime_contract import contract\n\n\ndef helper():\n    @contract\n    def inner():\n        pass\n"
        )
        self.assertEqual([], markers.contracts(path))
        self.assertEqual(1, markers.main(["dormant", path]))

    def run_task(self, text: str) -> subprocess.CompletedProcess:
        # PyYAML comes from uv here, as in scripts/main-tests.sh; make unit-test does not provide it.
        command = ["uv", "run", "--no-project", "--quiet", "--with", "pyyaml", "python3", str(HELPER), "task"]
        return subprocess.run([*command, self.write(text, "task.md")], capture_output=True, text=True, check=False)

    def task(self, front: str) -> list[str]:
        result = self.run_task(f"---\n{front}---\n\n# body\n")
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout.splitlines()

    def test_task_lists_id_tier_and_declared_modules(self) -> None:
        lines = self.task(
            "task_id: t-a01\ntier: review\nallowed_files:\n  - scripts/a.sh\n  - tests/unit/test_b.py\n"
            "  - tests/unit/regime_contract.py\n  - tests/unit/sub/test_c.py\n"
        )
        self.assertEqual(["task_id\tt-a01", "tier\treview", "module\ttests/unit/test_b.py"], lines)

    def test_a_missing_or_unknown_tier_is_design(self) -> None:
        for stamp in ("", "tier: Design\n", "tier: docs-ish\n"):
            with self.subTest(stamp=stamp):
                self.assertIn("tier\tdesign", self.task(f"task_id: t\n{stamp}allowed_files: []\n"))

    def test_design_scripts_need_their_module(self) -> None:
        lines = self.task(
            "task_id: t\nallowed_files:\n"
            "  - scripts/require-crit-review.py\n  - tests/unit/test_require_crit_review.py\n"
            "  - home/dot_local/bin/common/executable_herdr-agents\n"
            "  - home/.chezmoiscripts/run_once_x-y.sh.tmpl\n  - setup.sh\n"
            "  - scripts/legacy-task-ids.txt\n  - install/a/b.json\n  - README.md\n"
        )
        uncovered = [line for line in lines if line.startswith("uncovered")]
        self.assertEqual(
            [
                "uncovered\thome/dot_local/bin/common/executable_herdr-agents\ttests/unit/test_herdr_agents.py",
                "uncovered\thome/.chezmoiscripts/run_once_x-y.sh.tmpl\ttests/unit/test_run_once_x_y.py",
                "uncovered\tsetup.sh\ttests/unit/test_setup.py",
            ],
            uncovered,
        )
        review = self.task("task_id: t\ntier: review\nallowed_files:\n  - setup.sh\n")
        self.assertEqual([], [line for line in review if line.startswith("uncovered")])

    def test_malformed_task_files_fail_closed(self) -> None:
        for front in ("allowed_files: []\n", "task_id: t\n", "task_id: t\nallowed_files: [1]\n", "- a\n"):
            for text in (f"---\n{front}---\n", front):
                with self.subTest(text=text):
                    result = self.run_task(text)
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("main-tests: ", result.stderr)

    def test_scripts_filters_script_paths(self) -> None:
        paths = "scripts/a.sh\nhome/dot_local/bin/x\ninstall/y\nhome/.chezmoiscripts/z\nsetup.sh\nREADME.md\nhome/dot_zshrc\nsetup.sh.bak\n"
        out = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO(paths)), redirect_stdout(out):
            self.assertEqual(0, markers.main(["scripts"]))
        self.assertEqual(
            "scripts/a.sh\nhome/dot_local/bin/x\ninstall/y\nhome/.chezmoiscripts/z\nsetup.sh\n", out.getvalue()
        )


if __name__ == "__main__":
    unittest.main()
