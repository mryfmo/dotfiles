"""Exercise the uv phase of upgrade-tools.sh with a fake uv and a fixture manifest only."""

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UPGRADER = ROOT / "scripts/upgrade-tools.sh"
# Like uv 0.13, the fake colours each tool line when FORCE_COLOR or CLICOLOR_FORCE is set, unless --color never.
FAKE_UV = r"""#!/usr/bin/env bash
printf '%s\n' "$*" >> "${CALLS}"
if [ "$1 $2" = "tool list" ] && [ -n "${TOOLS}" ]; then
    while IFS= read -r line; do
        case "${line}:$*" in
        -* | :* | *--color\ never) printf '%s\n' "${line}" ;;
        *) [ -z "${FORCE_COLOR:-}${CLICOLOR_FORCE:-}" ] && printf '%s\n' "${line}" || printf '\033[1m%s\033[0m\n' "${line}" ;;
        esac
    done <<< "${TOOLS}"
fi
[ "$*" != "${FAIL:-}" ]
"""
TOOLS = "hcom v0.7.30\n- hcom\nruff v0.14.0\n- ruff\n"
WHEEL_PINNED = """schema_version: 1
assets:
  omp:
    upstream: https://registry.npmjs.org/omp-18.11.3.tgz
    pin: 18.11.3
  hcom:
    upstream: https://pypi.org/project/hcom/0.7.30/#files
    pin: 0.7.30
    files:
      linux-amd64: https://files.pythonhosted.org/hcom-0.7.30-py3-none-manylinux_2_17_x86_64.whl
"""


import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes, scratch_env


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


class UpgradeUvToolsTest(unittest.TestCase):
    def run_phase(self, tools, manifest=WHEEL_PINNED, fail=""):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            uv = root / "bin/uv"
            uv.parent.mkdir()
            uv.write_text(FAKE_UV)
            uv.chmod(0o755)
            config = root / "home/dot_agents/agent-config.yaml"
            config.parent.mkdir(parents=True)
            config.write_text(manifest)
            calls = root / "calls"
            calls.touch()
            result = subprocess.run(
                ["bash", "-c", 'source "$1"; repo_root="$2"; upgrade_uv_tools', "bash", str(UPGRADER), directory],
                env=os.environ
                | scratch_env(Path(directory))
                | {
                    "PATH": str(uv.parent) + os.pathsep + os.environ["PATH"],
                    "CALLS": str(calls),
                    "TOOLS": tools,
                    "FAIL": fail,
                    # A terminal pane may export both, and make update runs there.
                    "FORCE_COLOR": "1",
                    "CLICOLOR_FORCE": "1",
                },
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            return result, calls.read_text().splitlines()

    def test_a_tool_the_manifest_pins_from_a_wheel_is_skipped_and_the_others_upgraded(self):
        result, calls = self.run_phase(TOOLS)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("skip: hcom (manifest pins 0.7.30 from a wheel)", result.stdout)
        self.assertEqual(["tool list --color never", "tool upgrade ruff"], calls)

    def test_without_a_wheel_pin_every_tool_is_upgraded_and_one_failure_fails_the_phase(self):
        manifest = WHEEL_PINNED.split("    files:")[0]
        result, calls = self.run_phase(TOOLS, manifest)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("skip:", result.stdout)
        self.assertEqual(["tool list --color never", "tool upgrade hcom", "tool upgrade ruff"], calls)
        result, calls = self.run_phase(TOOLS, manifest, fail="tool upgrade hcom")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertEqual(["tool list --color never", "tool upgrade hcom", "tool upgrade ruff"], calls)

    def test_an_empty_tool_list_upgrades_nothing(self):
        result, calls = self.run_phase("")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(["tool list --color never"], calls)

    def test_the_repository_manifest_pins_hcom_from_a_wheel_at_the_rendered_pin(self):
        rendered = re.search(
            r'^HCOM_PIN_VERSION="([^"]+)"', (ROOT / "scripts/lib/installer-pins.sh").read_text(), re.MULTILINE
        )
        for tool, pin in (("hcom", rendered.group(1)), ("omp", "")):
            with self.subTest(tool=tool):
                result = subprocess.run(
                    ["bash", "-c", 'source "$1"; manifest_wheel_pin "$2"', "bash", str(UPGRADER), tool],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(pin, result.stdout.strip())


class PlatformPredicateTest(unittest.TestCase):
    def test_a_failed_uname_exits_the_script_instead_of_reading_as_another_os(self):
        for predicate, os_name in (("is_macos", "macOS"), ("is_linux", "Linux")):
            with self.subTest(predicate=predicate):
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        f'source "$1"; uname() {{ return 1; }}; if ! {predicate}; then echo "other OS"; fi',
                        "bash",
                        str(UPGRADER),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertEqual(f"uname failed; cannot tell whether this host is {os_name}\n", result.stderr)
                self.assertNotIn("other OS", result.stdout)

    def test_a_failed_dirname_stops_the_script_and_the_mise_self_update(self):
        # A failed dirname used to resolve the repository root, or the mise prefix, to /.
        with tempfile.TemporaryDirectory() as directory:
            bin_dir = Path(directory)
            for name, body in (("dirname", "exit 1\n"), ("mise", "echo mise-ran\n")):
                (bin_dir / name).write_text("#!/usr/bin/env bash\n" + body)
                (bin_dir / name).chmod(0o755)
            for label, script, env, message in (
                ("root", 'source "$1"', {"PATH": f"{bin_dir}:/usr/bin:/bin"}, "upgrade-tools: dirname failed on"),
                (
                    "mise prefix",
                    'source "$1"; dirname() { return 1; }; upgrade_mise_self',
                    {"PATH": f"{bin_dir}:{os.environ['PATH']}"},
                    "",
                ),
            ):
                with self.subTest(label=label):
                    result = subprocess.run(
                        ["bash", "-c", script, "bash", str(UPGRADER)],
                        env=os.environ | env,
                        capture_output=True,
                        text=True,
                        timeout=30,
                        check=False,
                    )
                    self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                    self.assertIn(message, result.stderr)
                    self.assertNotIn("mise self-update", result.stdout)
                    self.assertNotIn("mise-ran", result.stdout)


if __name__ == "__main__":
    unittest.main()
