#!/usr/bin/env python3
"""Exercise the Herdr agent workspace helper with fake CLIs."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_herdr-agents"
HERDR_CONFIG = ROOT / "home/dot_config/herdr/config.toml"
GHOSTTY_CONFIG = ROOT / "home/dot_config/ghostty/config.ghostty.tmpl"
ZSHRC = ROOT / "home/dot_zshrc"


class HerdrAgentsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="herdr-agents-test-"))
        self.bin_dir = self.temp_dir / "bin"
        self.bin_dir.mkdir()
        self.calls_path = self.temp_dir / "herdr-calls.txt"
        self.workdir = self.temp_dir / "project"
        self.workdir.mkdir()

        self.write_executable(
            "herdr",
            f"""#!/usr/bin/env bash
printf '%s\\n' "$*" >> {self.calls_path}
if [[ $1 == workspace && $2 == create ]]; then
    printf '%s\\n' '{{"id":"cli:workspace:create","result":{{"root_pane":{{"pane_id":"w-test:p1"}},"workspace":{{"workspace_id":"w-test"}}}}}}'
fi
""",
        )
        self.write_executable("claude", "#!/usr/bin/env bash\n")
        self.write_executable("codex", "#!/usr/bin/env bash\n")

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_executable(self, name: str, content: str) -> None:
        path = self.bin_dir / name
        path.write_text(textwrap.dedent(content))
        path.chmod(0o755)

    def run_helper(self) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PATH"] = f"{self.bin_dir}{os.pathsep}{env['PATH']}"
        return subprocess.run(
            ["bash", str(SCRIPT), str(self.workdir)],
            cwd=ROOT,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_uses_initial_workspace_pane_for_claude_and_splits_codex_below(self) -> None:
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn("pane run w-test:p1 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude", calls)
        self.assertIn(
            f"agent start codex --cwd {self.workdir} --workspace w-test --split down --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- codex",
            calls,
        )
        self.assertNotIn(
            f"agent start claude --cwd {self.workdir} --workspace w-test --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --focus -- claude",
            calls,
        )

    def test_herdr_prefix_alt_a_runs_helper_from_active_pane(self) -> None:
        config = tomllib.loads(HERDR_CONFIG.read_text())
        command = next(item for item in config["keys"]["command"] if item["key"] == "prefix+alt+a")

        self.assertEqual(command["type"], "shell")
        self.assertEqual(command["command"], 'herdr-agents "${HERDR_ACTIVE_PANE_CWD:-$PWD}"')

    def run_zshrc_herdr(self, command: str, *, ghostty: bool) -> subprocess.CompletedProcess[str]:
        self.write_executable(
            "sheldon",
            "#!/usr/bin/env bash\nif [[ ${1:-} == source ]]; then exit 0; fi\n",
        )
        self.write_executable(
            "herdr-agents",
            f"""#!/usr/bin/env bash
printf 'herdr-agents %s\\n' "$1" >> {self.calls_path}
""",
        )
        self.write_executable(
            "herdr",
            f"""#!/usr/bin/env bash
printf 'herdr %s\\n' "$*" >> {self.calls_path}
""",
        )

        env = os.environ.copy()
        env["PATH"] = f"{self.bin_dir}{os.pathsep}{env['PATH']}"
        if ghostty:
            env["GHOSTTY_RESOURCES_DIR"] = str(self.temp_dir / "ghostty")
        else:
            env.pop("GHOSTTY_RESOURCES_DIR", None)

        return subprocess.run(
            ["zsh", "-fc", f"source {ZSHRC}; {command}"],
            cwd=self.workdir,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_ghostty_config_keeps_normal_shell_startup(self) -> None:
        self.assertNotIn("initial-command", GHOSTTY_CONFIG.read_text())

    def test_bare_herdr_in_ghostty_starts_agent_layout(self) -> None:
        result = self.run_zshrc_herdr("herdr", ghostty=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            [f"herdr-agents {self.workdir.resolve()}"],
        )

    def test_herdr_with_args_in_ghostty_uses_real_cli(self) -> None:
        result = self.run_zshrc_herdr("herdr server reload-config", ghostty=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            ["herdr server reload-config"],
        )

    def test_bare_herdr_outside_ghostty_uses_real_cli(self) -> None:
        result = self.run_zshrc_herdr("herdr", ghostty=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            ["herdr "],
        )


if __name__ == "__main__":
    unittest.main()
