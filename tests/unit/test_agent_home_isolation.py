"""Guard: no test that runs an agent-asset script can reach the operator's real agent or gh directories."""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
import agent_home_isolation as iso

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = re.compile(
    r"update-agent-assets\.sh|upgrade-tools\.sh|gh_extensions\.sh|pin_records\.py|check-agent-runtime\.py"
)


def harness_modules() -> list[Path]:
    """Unit modules that start a subprocess and name one of the scripts that resolve agent homes."""
    return [
        path
        for path in sorted((ROOT / "tests/unit").glob("test_*.py"))
        if path.name != Path(__file__).name and SCRIPTS.search(text := path.read_text()) and "subprocess" in text
    ]


def module_hook_calls(path: Path) -> dict[str, set[str]]:
    hooks: dict[str, set[str]] = {}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.FunctionDef) and node.name in {"setUpModule", "tearDownModule"}:
            hooks[node.name] = {
                call.func.id
                for call in ast.walk(node)
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
            }
    return hooks


class HarnessCoverageTest(unittest.TestCase):
    def test_every_python_harness_isolates_the_agent_homes_for_the_whole_module(self) -> None:
        modules = harness_modules()
        self.assertIn("test_update_agent_assets.py", {path.name for path in modules})
        missing = []
        for path in modules:
            hooks = module_hook_calls(path)
            if "isolate_agent_homes" not in hooks.get("setUpModule", set()):
                missing.append(f"{path.name}: setUpModule does not call isolate_agent_homes")
            if "restore_agent_homes" not in hooks.get("tearDownModule", set()):
                missing.append(f"{path.name}: tearDownModule does not call restore_agent_homes")
        self.assertEqual([], missing)

    def test_every_bats_file_that_runs_a_script_isolates_all_six_in_setup(self) -> None:
        runners = [
            path
            for path in sorted((ROOT / "tests").rglob("*.bats"))
            if re.search(
                r"(source|bash) \"?(\$\{SCRIPT_PATH\}|\./)?[\w/.-]*(" + SCRIPTS.pattern + ")", path.read_text()
            )
            or re.search(r'SCRIPT_PATH="[^"]*(' + SCRIPTS.pattern + ')"', path.read_text())
        ]
        self.assertIn(ROOT / "tests/install/common/gh_extensions.bats", runners)
        for path in runners:
            with self.subTest(path.name):
                self.assertEqual(sorted(iso.VARIABLES), sorted(self.bats_setup_env(path)))

    def bats_setup_env(self, path: Path) -> dict[str, str]:
        """Run the file's setup() with every variable inherited from a pretend real home; return what it exports."""
        match = re.search(r"^setup\(\) \{\n.*?^\}\n", path.read_text(), re.M | re.S)
        self.assertIsNotNone(match, f"{path.name} has no setup()")
        with tempfile.TemporaryDirectory() as scratch:
            real = "/Users/operator"
            result = subprocess.run(
                [
                    "bash",
                    "-c",
                    match.group(0) + 'setup; for n in "$@"; do printf "%s=%s\\n" "$n" "${!n}"; done',
                    "bash",
                    *iso.VARIABLES,
                ],
                env={"PATH": os.environ["PATH"], "BATS_TEST_TMPDIR": scratch}
                | {name: f"{real}/{name.lower()}" for name in iso.VARIABLES},
                text=True,
                capture_output=True,
                check=True,
            )
            exported = dict(line.split("=", 1) for line in result.stdout.splitlines())
            outside = {name: value for name, value in exported.items() if not value.startswith(scratch + "/")}
        self.assertEqual({}, outside)
        return exported


class HelperTest(unittest.TestCase):
    def test_assert_isolated_refuses_an_unset_or_inherited_variable(self) -> None:
        good = iso.scratch_env(Path(tempfile.gettempdir()) / "fixture-home")
        iso.assert_isolated(good)
        for name in iso.VARIABLES:
            with self.subTest(name), self.assertRaisesRegex(AssertionError, name):
                iso.assert_isolated(good | {name: ""})
            with self.subTest(name), self.assertRaisesRegex(AssertionError, name):
                iso.assert_isolated(good | {name: "/Users/operator/.local/share/gh"})

    def test_scratch_env_keeps_gh_data_under_an_overridden_xdg_data_home(self) -> None:
        home = Path(tempfile.gettempdir()) / "fixture-home"
        env = iso.scratch_env(home, XDG_DATA_HOME=str(home / "data"))
        self.assertEqual(str(home / "data/gh"), env["GH_DATA_DIR"])

    def test_isolate_replaces_every_inherited_variable_and_restore_puts_it_back(self) -> None:
        inherited = {name: f"/Users/operator/{name.lower()}" for name in iso.VARIABLES}
        with mock.patch.dict(os.environ, inherited):
            home = iso.isolate_agent_homes()
            try:
                self.assertEqual(str(home), os.environ["HOME"])
                self.assertTrue(iso.under_scratch(os.environ["HOME"]))
                self.assertEqual([], [name for name in iso.VARIABLES[1:] if name in os.environ])
                iso.assert_isolated(iso.complete_env(os.environ))
            finally:
                iso.restore_agent_homes()
            self.assertEqual(inherited, {name: os.environ[name] for name in iso.VARIABLES})
            self.assertFalse(home.exists())


if __name__ == "__main__":
    unittest.main()
