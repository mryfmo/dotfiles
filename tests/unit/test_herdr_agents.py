#!/usr/bin/env python3
"""Exercise the Herdr agent workspace helper with fake CLIs."""

from __future__ import annotations

import errno
import os
import pty
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
GHOSTTY_CONFIG = ROOT / "home/dot_config/ghostty/config"
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
if [[ $1 == agent && $2 == start ]]; then
    printf '%s\\n' '{{"id":"cli:agent:start","result":{{"pane":{{"pane_id":"w-test:p2"}}}}}}'
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

    def materialize_agmsg_scripts(self) -> Path:
        source = ROOT / "home/dot_agents/skills/agmsg/scripts"
        target = self.temp_dir / "agmsg" / "scripts"
        shutil.copytree(source, target)
        for path in target.rglob("executable_*.sh"):
            installed = path.with_name(path.name.removeprefix("executable_"))
            shutil.copy2(path, installed)
            installed.chmod(0o755)
        return target

    def install_zshrc_fakes(self) -> None:
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
        self.assertIn("pane rename w-test:p1 claude-orchestrator", calls)
        self.assertIn("pane run w-test:p1 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high", calls)
        self.assertIn(
            f"agent start codex-worker-w-test --cwd {self.workdir} --workspace w-test --split down --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- codex --sandbox workspace-write -m gpt-5.5 -c model_reasoning_effort=high",
            calls,
        )
        self.assertIn("pane rename w-test:p2 codex-worker", calls)
        self.assertNotIn(
            f"agent start claude --cwd {self.workdir} --workspace w-test --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --focus -- claude",
            calls,
        )

    def test_ghostty_herdr_starts_stacked_agents_with_working_agmsg(self) -> None:
        agmsg_scripts = self.materialize_agmsg_scripts()
        agmsg_storage = self.temp_dir / "agmsg-db"
        agmsg_storage.mkdir()
        e2e_log = self.temp_dir / "e2e.log"

        self.write_executable(
            "herdr-agents",
            f"""#!/usr/bin/env bash
printf 'herdr-agents %s\\n' "$1" >> {self.calls_path}
exec bash {SCRIPT} "$@"
""",
        )
        self.write_executable(
            "herdr",
            f"""#!/usr/bin/env bash
set -euo pipefail
printf 'herdr %s\\n' "$*" >> {self.calls_path}
if [[ $# -eq 0 ]]; then
    printf 'attached workspace from cwd=%s\\n' "$PWD" >> {e2e_log}
    exit 0
fi
if [[ $1 == workspace && $2 == create ]]; then
    printf '%s\\n' '{{"id":"cli:workspace:create","result":{{"root_pane":{{"pane_id":"w-test:p1"}},"workspace":{{"workspace_id":"w-test"}}}}}}'
    exit 0
fi
if [[ $1 == pane && $2 == run ]]; then
    printf 'top pane=%s cwd=%s command=%s\\n' "$3" "$PWD" "$4" >> {e2e_log}
    bash -c "$4"
    exit 0
fi
if [[ $1 == pane && $2 == rename ]]; then
    exit 0
fi
if [[ $1 == agent && $2 == start ]]; then
    cwd=''
    workspace=''
    split=''
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --cwd) cwd="$2"; shift 2 ;;
            --workspace) workspace="$2"; shift 2 ;;
            --split) split="$2"; shift 2 ;;
            --) shift; break ;;
            *) shift ;;
        esac
    done
    printf 'bottom workspace=%s split=%s cwd=%s command=%s\\n' "$workspace" "$split" "$cwd" "$*" >> {e2e_log}
    (cd "$cwd" && "$@")
    printf '%s\\n' '{{"id":"cli:agent:start","result":{{"pane":{{"pane_id":"w-test:p2"}}}}}}'
    exit 0
fi
""",
        )
        self.write_executable(
            "claude",
            f"""#!/usr/bin/env bash
set -euo pipefail
printf 'claude cwd=%s\\n' "$PWD" >> {e2e_log}
{agmsg_scripts}/join.sh ghostty-e2e claude-code claude-code "$PWD" > /dev/null
{agmsg_scripts}/send.sh ghostty-e2e claude-code codex "ready from claude" > /dev/null
""",
        )
        self.write_executable(
            "codex",
            f"""#!/usr/bin/env bash
set -euo pipefail
printf 'codex cwd=%s\\n' "$PWD" >> {e2e_log}
{agmsg_scripts}/join.sh ghostty-e2e codex codex "$PWD" > /dev/null
{agmsg_scripts}/inbox.sh ghostty-e2e codex >> {e2e_log}
""",
        )

        env = os.environ.copy()
        for key in tuple(env):
            if key.startswith(("GHOSTTY_", "HERDR_")):
                env.pop(key)
        env.pop("TERM_PROGRAM", None)
        env["PATH"] = f"{self.bin_dir}{os.pathsep}{env['PATH']}"
        env["AGMSG_STORAGE_PATH"] = str(agmsg_storage)
        env["GHOSTTY_RESOURCES_DIR"] = str(self.temp_dir / "ghostty")
        result = subprocess.run(
            ["zsh", "-fc", f"source {ZSHRC}; herdr"],
            cwd=self.workdir,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            [
                f"herdr-agents {self.workdir.resolve()}",
                f"herdr workspace create --cwd {self.workdir.resolve()} --label project agents --focus",
                "herdr pane rename w-test:p1 claude-orchestrator",
                "herdr pane run w-test:p1 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high",
                f"herdr agent start codex-worker-w-test --cwd {self.workdir.resolve()} --workspace w-test --split down --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- codex --sandbox workspace-write -m gpt-5.5 -c model_reasoning_effort=high",
                "herdr pane rename w-test:p2 codex-worker",
                "herdr ",
            ],
        )
        e2e_lines = e2e_log.read_text()
        self.assertIn(f"top pane=w-test:p1 cwd={self.workdir.resolve()} command=CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high", e2e_lines)
        self.assertIn(f"bottom workspace=w-test split=down cwd={self.workdir.resolve()} command=codex --sandbox workspace-write -m gpt-5.5 -c model_reasoning_effort=high", e2e_lines)
        self.assertIn(f"claude cwd={self.workdir.resolve()}", e2e_lines)
        self.assertIn(f"codex cwd={self.workdir.resolve()}", e2e_lines)
        self.assertIn("1 new message(s):", e2e_lines)
        self.assertIn("claude-code", e2e_lines)
        self.assertIn("ready from claude", e2e_lines)

    def test_herdr_prefix_alt_a_runs_helper_from_active_pane(self) -> None:
        config = tomllib.loads(HERDR_CONFIG.read_text())
        command = next(item for item in config["keys"]["command"] if item["key"] == "prefix+alt+a")

        self.assertEqual(command["type"], "shell")
        self.assertEqual(command["command"], 'herdr-agents "${HERDR_ACTIVE_PANE_CWD:-$PWD}"')

    def run_zshrc_herdr(self, command: str, *, ghostty: bool) -> subprocess.CompletedProcess[str]:
        self.install_zshrc_fakes()
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

    def run_interactive_ghostty_herdr(self) -> subprocess.CompletedProcess[str]:
        self.install_zshrc_fakes()
        env = os.environ.copy()
        env["PATH"] = f"{self.bin_dir}{os.pathsep}{env['PATH']}"
        env["GHOSTTY_RESOURCES_DIR"] = str(self.temp_dir / "ghostty")

        master_fd, slave_fd = pty.openpty()
        try:
            proc = subprocess.Popen(
                ["zsh", "-ifc", f"source {ZSHRC}; herdr"],
                cwd=self.workdir,
                env=env,
                text=True,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
            )
        finally:
            os.close(slave_fd)

        output = []
        with os.fdopen(master_fd, "r", errors="replace") as tty:
            while True:
                try:
                    chunk = tty.read()
                except OSError as error:
                    if error.errno != errno.EIO:
                        raise
                    break
                if not chunk:
                    break
                output.append(chunk)

        return subprocess.CompletedProcess(
            proc.args,
            proc.wait(),
            "".join(output),
            "",
        )

    def test_ghostty_config_keeps_normal_shell_startup(self) -> None:
        self.assertNotIn("initial-command", GHOSTTY_CONFIG.read_text())

    def test_bare_herdr_in_ghostty_starts_agent_layout(self) -> None:
        result = self.run_zshrc_herdr("herdr", ghostty=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            [f"herdr-agents {self.workdir.resolve()}", "herdr "],
        )

    def test_interactive_ghostty_shell_attaches_after_agent_layout(self) -> None:
        result = self.run_interactive_ghostty_herdr()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            [f"herdr-agents {self.workdir.resolve()}", "herdr "],
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
