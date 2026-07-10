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
HERDR_SESSION_SCRIPT = ROOT / "home/dot_local/bin/common/executable_herdr-session"
HERDR_CONFIG = ROOT / "home/dot_config/herdr/config.toml"
YAZI_CONFIG = ROOT / "home/dot_config/yazi/yazi.toml"
GHOSTTY_CONFIG = ROOT / "home/dot_config/ghostty/config"
ZPROFILE = ROOT / "home/dot_zprofile"
ZSHRC = ROOT / "home/dot_zshrc"


class HerdrAgentsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="herdr-agents-test-"))
        self.bin_dir = self.temp_dir / "bin"
        self.bin_dir.mkdir()
        self.calls_path = self.temp_dir / "herdr-calls.txt"
        self.workspace_list_path = self.temp_dir / "workspace-list.json"
        self.pane_list_path = self.temp_dir / "pane-list.json"
        self.agent_get_path = self.temp_dir / "agent-get.json"
        self.pane_counter_path = self.temp_dir / "pane-counter.txt"
        self.home_dir = self.temp_dir / "home"
        (self.home_dir / ".config/herdr").mkdir(parents=True)
        self.workdir = self.temp_dir / "project"
        self.workdir.mkdir()
        self.workspace_list_path.write_text('{"id":"cli:workspace:list","result":{"type":"workspace_list","workspaces":[]}}\n')
        self.pane_list_path.write_text('{"id":"cli:pane:list","result":{"panes":[]}}\n')
        self.agent_get_path.write_text("")
        self.pane_counter_path.write_text("2\n")

        self.write_executable(
            "herdr",
            f"""#!/usr/bin/env bash
printf '%s\\n' "$*" >> {self.calls_path}
if [[ $1 == workspace && $2 == list ]]; then
    cat {self.workspace_list_path}
    exit 0
fi
if [[ $1 == workspace && $2 == create ]]; then
    printf '%s\\n' '{{"id":"cli:workspace:create","result":{{"root_pane":{{"pane_id":"w-test:p1"}},"workspace":{{"workspace_id":"w-test"}}}}}}'
    exit 0
fi
if [[ $1 == workspace && $2 == focus ]]; then
    exit 0
fi
if [[ $1 == pane && $2 == list ]]; then
    cat {self.pane_list_path}
    exit 0
fi
if [[ $1 == pane && $2 == split ]]; then
    workspace="${{3%%:*}}"
    pane_number="$(( $(cat {self.pane_counter_path}) + 1 ))"
    printf '%s\\n' "$pane_number" > {self.pane_counter_path}
    printf '{{"id":"cli:pane:split","result":{{"pane":{{"pane_id":"%s:p%s"}}}}}}\\n' "$workspace" "$pane_number"
    exit 0
fi
if [[ $1 == pane && $2 == swap ]]; then
    exit 0
fi
if [[ $1 == agent && $2 == start ]]; then
    workspace='w-test'
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --workspace) workspace="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    printf '{{"id":"cli:agent:start","result":{{"pane":{{"pane_id":"%s:p2"}}}}}}\\n' "$workspace"
    exit 0
fi
if [[ $1 == agent && $2 == get ]]; then
    if [[ -s {self.agent_get_path} ]]; then
        cat {self.agent_get_path}
        exit 0
    fi
    exit 1
fi
""",
        )
        self.write_executable("claude", "#!/usr/bin/env bash\n")
        self.write_executable("codex", "#!/usr/bin/env bash\n")
        self.write_executable("yazi", "#!/usr/bin/env bash\n")

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

    def install_zshrc_fakes(self, *, herdr_session_exit_code: int = 0) -> None:
        self.write_executable(
            "sheldon",
            "#!/usr/bin/env bash\nif [[ ${1:-} == source ]]; then exit 0; fi\n",
        )
        self.write_executable(
            "herdr-session",
            f"""#!/usr/bin/env bash
printf 'herdr-session %s\\n' "$*" >> {self.calls_path}
exit {herdr_session_exit_code}
""",
        )
        self.write_executable(
            "herdr",
            f"""#!/usr/bin/env bash
printf 'herdr %s\\n' "$*" >> {self.calls_path}
""",
        )

    def write_workspace_state(self, workspace_id: str, panes: str, *, agent_pane_id: str = "") -> None:
        self.workspace_list_path.write_text(
            textwrap.dedent(
                f"""\
                {{"id":"cli:workspace:list","result":{{"type":"workspace_list","workspaces":[
                    {{"active_tab_id":"{workspace_id}:t1","agent_status":"working","focused":false,"label":"project agents","number":1,"pane_count":2,"tab_count":1,"workspace_id":"{workspace_id}"}}
                ]}}}}
                """
            )
        )
        self.pane_list_path.write_text(f'{{"id":"cli:pane:list","result":{{"panes":[{panes}]}}}}\n')
        if agent_pane_id:
            self.agent_get_path.write_text(f'{{"id":"cli:agent:get","result":{{"agent":{{"pane_id":"{agent_pane_id}"}},"type":"agent_info"}}}}\n')
        else:
            self.agent_get_path.write_text("")

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

    def run_session_helper(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(self.home_dir)
        env["PATH"] = f"{self.bin_dir}{os.pathsep}{env['PATH']}"
        return subprocess.run(
            ["bash", str(HERDR_SESSION_SCRIPT), *args],
            cwd=self.workdir,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_uses_initial_workspace_pane_for_claude_and_splits_codex_right(self) -> None:
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn("pane rename w-test:p1 claude-orchestrator", calls)
        self.assertIn("pane run w-test:p1 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high", calls)
        self.assertIn(
            f"agent start codex-worker-w-test --cwd {self.workdir} --workspace w-test --split right --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- codex --sandbox workspace-write -m gpt-5.6-sol -c model_reasoning_effort=high",
            calls,
        )
        self.assertIn("pane rename w-test:p2 codex-worker", calls)
        self.assertIn(f"pane split w-test:p1 --direction right --ratio 0.8 --cwd {self.workdir} --no-focus", calls)
        self.assertIn("pane rename w-test:p3 files", calls)
        self.assertIn("pane run w-test:p3 yazi", calls)
        self.assertNotIn(
            f"agent start claude --cwd {self.workdir} --workspace w-test --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --focus -- claude",
            calls,
        )

    def test_existing_agents_workspace_focuses_without_recreating_agents(self) -> None:
        self.write_workspace_state(
            "w-old",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-old:p1","workspace_id":"w-old"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-old:p2","workspace_id":"w-old"}},'
            f'{{"agent":null,"cwd":"{self.workdir}","label":"files","pane_id":"w-old:p9","workspace_id":"w-old"}}',
            agent_pane_id="w-old:p2",
        )

        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn("workspace focus w-old", calls)
        self.assertNotIn(f"workspace create --cwd {self.workdir} --label project agents --focus", calls)
        self.assertFalse(any(call.startswith("agent start ") for call in calls))
        self.assertFalse(any(call.startswith("pane split ") for call in calls))

    def test_existing_workspace_adds_missing_files_pane(self) -> None:
        self.write_workspace_state(
            "w-old",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-old:p1","workspace_id":"w-old"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-old:p2","workspace_id":"w-old"}}',
            agent_pane_id="w-old:p2",
        )

        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn(f"pane split w-old:p2 --direction right --ratio 0.6 --cwd {self.workdir} --no-focus", calls)
        self.assertIn("pane rename w-old:p3 files", calls)
        self.assertIn("pane run w-old:p3 yazi", calls)

    def test_existing_files_pane_is_not_reused_for_claude_or_split_again(self) -> None:
        self.write_workspace_state(
            "w-old",
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-old:p2","workspace_id":"w-old"}},'
            f'{{"agent":null,"cwd":"{self.workdir}","label":"files","pane_id":"w-old:p9","workspace_id":"w-old"}}',
            agent_pane_id="w-old:p2",
        )

        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn("pane split w-old:p2 --direction right --no-focus", calls)
        self.assertIn("pane run w-old:p3 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high", calls)
        self.assertFalse(any("--ratio" in call for call in calls))
        self.assertFalse(any(call.startswith("pane rename w-old:p9 ") for call in calls))
        self.assertFalse(any(call.startswith("pane run w-old:p9 ") for call in calls))

    def test_existing_workspace_restarts_missing_codex_agent(self) -> None:
        self.write_workspace_state(
            "w-old",
            f'{{"agent":"claude","cwd":"{self.workdir}","pane_id":"w-old:p1","workspace_id":"w-old"}}',
        )

        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn(
            f"agent start codex-worker-w-old --cwd {self.workdir} --workspace w-old --split right --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- codex --sandbox workspace-write -m gpt-5.6-sol -c model_reasoning_effort=high",
            calls,
        )
        self.assertIn("pane rename w-old:p2 codex-worker", calls)
        self.assertNotIn(f"workspace create --cwd {self.workdir} --label project agents --focus", calls)
        self.assertIn("workspace focus w-old", calls)

    def test_claude_repair_skips_just_restarted_codex_pane_without_agent_field(self) -> None:
        self.write_workspace_state(
            "w-old",
            f'{{"agent":null,"cwd":"{self.workdir}","pane_id":"w-old:p2","workspace_id":"w-old"}},'
            f'{{"agent":null,"cwd":"{self.workdir}","pane_id":"w-old:p3","workspace_id":"w-old"}}',
        )

        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn(
            f"agent start codex-worker-w-old --cwd {self.workdir} --workspace w-old --split right --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- codex --sandbox workspace-write -m gpt-5.6-sol -c model_reasoning_effort=high",
            calls,
        )
        self.assertIn("pane run w-old:p3 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high", calls)
        self.assertNotIn("pane run w-old:p2 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high", calls)

    def test_existing_workspace_restarts_missing_claude_in_empty_pane(self) -> None:
        self.write_workspace_state(
            "w-old",
            f'{{"agent":null,"cwd":"{self.workdir}","pane_id":"w-old:p1","workspace_id":"w-old"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","pane_id":"w-old:p2","workspace_id":"w-old"}}',
            agent_pane_id="w-old:p2",
        )

        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn("pane rename w-old:p1 claude-orchestrator", calls)
        self.assertIn("pane run w-old:p1 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high", calls)
        self.assertFalse(any(call.startswith("agent start ") for call in calls))
        self.assertIn("workspace focus w-old", calls)

    def test_existing_workspace_splits_when_missing_claude_has_no_empty_pane(self) -> None:
        self.write_workspace_state(
            "w-old",
            f'{{"agent":"codex","cwd":"{self.workdir}","pane_id":"w-old:p2","workspace_id":"w-old"}}',
            agent_pane_id="w-old:p2",
        )

        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn("pane split w-old:p2 --direction right --no-focus", calls)
        self.assertIn("pane swap --pane w-old:p3 --direction left", calls)
        self.assertIn("pane run w-old:p3 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high", calls)
        self.assertIn("workspace focus w-old", calls)

    def test_ghostty_herdr_starts_left_right_agents_with_working_agmsg(self) -> None:
        agmsg_scripts = self.materialize_agmsg_scripts()
        agmsg_storage = self.temp_dir / "agmsg-db"
        agmsg_storage.mkdir()
        e2e_log = self.temp_dir / "e2e.log"

        self.write_executable(
            "herdr-session",
            f"""#!/usr/bin/env bash
printf 'herdr-session %s\\n' "$*" >> {self.calls_path}
exec bash {HERDR_SESSION_SCRIPT}
""",
        )
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
if [[ $1 == workspace && $2 == list ]]; then
    printf '%s\\n' '{{"id":"cli:workspace:list","result":{{"type":"workspace_list","workspaces":[]}}}}'
    exit 0
fi
if [[ $1 == workspace && $2 == create ]]; then
    printf '%s\\n' '{{"id":"cli:workspace:create","result":{{"root_pane":{{"pane_id":"w-test:p1"}},"workspace":{{"workspace_id":"w-test"}}}}}}'
    exit 0
fi
if [[ $1 == pane && $2 == split ]]; then
    printf '%s\\n' '{{"id":"cli:pane:split","result":{{"pane":{{"pane_id":"w-test:p3"}}}}}}'
    exit 0
fi
if [[ $1 == pane && $2 == run ]]; then
    printf 'left pane=%s cwd=%s command=%s\\n' "$3" "$PWD" "$4" >> {e2e_log}
    if [[ $3 == w-test:p1 ]]; then
        bash -c "$4"
    fi
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
    printf 'right workspace=%s split=%s cwd=%s command=%s\\n' "$workspace" "$split" "$cwd" "$*" >> {e2e_log}
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
        env["HOME"] = str(self.home_dir)
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
                "herdr-session ",
                f"herdr-agents {self.workdir.resolve()}",
                "herdr workspace list",
                f"herdr workspace create --cwd {self.workdir.resolve()} --label project agents --focus",
                "herdr pane rename w-test:p1 claude-orchestrator",
                "herdr pane run w-test:p1 CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high",
                f"herdr pane split w-test:p1 --direction right --ratio 0.8 --cwd {self.workdir.resolve()} --no-focus",
                "herdr pane rename w-test:p3 files",
                "herdr pane run w-test:p3 yazi",
                f"herdr agent start codex-worker-w-test --cwd {self.workdir.resolve()} --workspace w-test --split right --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- codex --sandbox workspace-write -m gpt-5.6-sol -c model_reasoning_effort=high",
                "herdr pane rename w-test:p2 codex-worker",
                "herdr ",
            ],
        )
        e2e_lines = e2e_log.read_text()
        self.assertIn(f"left pane=w-test:p1 cwd={self.workdir.resolve()} command=CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high", e2e_lines)
        self.assertIn(f"right workspace=w-test split=right cwd={self.workdir.resolve()} command=codex --sandbox workspace-write -m gpt-5.6-sol -c model_reasoning_effort=high", e2e_lines)
        self.assertIn(f"claude cwd={self.workdir.resolve()}", e2e_lines)
        self.assertIn(f"codex cwd={self.workdir.resolve()}", e2e_lines)
        self.assertIn("1 new message(s):", e2e_lines)
        self.assertIn("claude-code", e2e_lines)
        self.assertIn("ready from claude", e2e_lines)

    def test_herdr_session_passes_syntax_check(self) -> None:
        result = subprocess.run(
            ["bash", "-n", str(HERDR_SESSION_SCRIPT)],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_herdr_session_runs_agents_then_execs_herdr(self) -> None:
        self.write_executable(
            "herdr-agents",
            f"""#!/usr/bin/env bash
printf 'herdr-agents %s\\n' "$1" >> {self.calls_path}
printf 'agents stdout\\n'
printf 'agents stderr\\n' >&2
""",
        )
        self.write_executable(
            "herdr",
            f"""#!/usr/bin/env bash
printf 'herdr %s\\n' "$*" >> {self.calls_path}
""",
        )

        result = self.run_session_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            [f"herdr-agents {self.workdir.resolve()}", "herdr "],
        )
        self.assertEqual(
            (self.home_dir / ".config/herdr/herdr-agents.log").read_text().splitlines(),
            ["agents stdout", "agents stderr"],
        )

    def test_herdr_session_attaches_after_agent_layout_failure(self) -> None:
        self.write_executable(
            "herdr-agents",
            f"""#!/usr/bin/env bash
printf 'herdr-agents %s\\n' "$1" >> {self.calls_path}
printf 'layout failed\\n' >&2
exit 42
""",
        )
        self.write_executable(
            "herdr",
            f"""#!/usr/bin/env bash
printf 'herdr %s\\n' "$*" >> {self.calls_path}
""",
        )

        result = self.run_session_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            [f"herdr-agents {self.workdir.resolve()}", "herdr "],
        )
        self.assertIn(
            f"herdr-agents failed; see {self.home_dir}/.config/herdr/herdr-agents.log",
            result.stderr,
        )
        self.assertEqual(
            (self.home_dir / ".config/herdr/herdr-agents.log").read_text().splitlines(),
            ["layout failed"],
        )

    def test_herdr_session_rejects_arguments(self) -> None:
        result = self.run_session_helper("extra")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("Usage: herdr-session", result.stderr)
        self.assertFalse(self.calls_path.exists())

    def test_herdr_prefix_alt_a_runs_helper_from_active_pane(self) -> None:
        config = tomllib.loads(HERDR_CONFIG.read_text())
        command = next(item for item in config["keys"]["command"] if item["key"] == "prefix+alt+a")

        self.assertEqual(command["type"], "shell")
        self.assertEqual(command["command"], 'herdr-agents "${HERDR_ACTIVE_PANE_CWD:-$PWD}"')

    def test_yazi_edit_opener_uses_existing_zed_workspace(self) -> None:
        config = tomllib.loads(YAZI_CONFIG.read_text())

        self.assertEqual(
            config["opener"]["edit"],
            [{"run": "zed --existing %s", "orphan": True, "for": "unix"}],
        )

    def run_zshrc_herdr(
        self,
        command: str,
        *,
        ghostty: bool,
        herdr_session_exit_code: int = 0,
    ) -> subprocess.CompletedProcess[str]:
        self.install_zshrc_fakes(herdr_session_exit_code=herdr_session_exit_code)
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

    def test_ghostty_config_does_not_auto_start_herdr_session(self) -> None:
        self.assertNotIn("initial-command", GHOSTTY_CONFIG.read_text())

    def test_zprofile_adds_common_bin_to_login_shell_path(self) -> None:
        zprofile = ZPROFILE.read_text()
        zshrc = ZSHRC.read_text()

        self.assertIn("typeset -gU path", zprofile)
        self.assertIn("${HOME}/.local/bin/common(N-/)", zprofile)
        self.assertNotIn("typeset -gU path fpath", zshrc)

    def test_bare_herdr_in_ghostty_starts_agent_layout(self) -> None:
        result = self.run_zshrc_herdr("herdr", ghostty=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            ["herdr-session "],
        )

    def test_interactive_ghostty_shell_attaches_after_agent_layout(self) -> None:
        result = self.run_interactive_ghostty_herdr()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            ["herdr-session "],
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
