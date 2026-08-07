#!/usr/bin/env python3
"""Exercise the Herdr agent workspace helper with fake CLIs."""

from __future__ import annotations

import errno
import json
import os
import pty
import shutil
import subprocess
import sys
import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_herdr-agents"
MAKEFILE = ROOT / "Makefile"
HERDR_SESSION_SCRIPT = ROOT / "home/dot_local/bin/common/executable_herdr-session"
CLAUDE_SETTINGS_MODIFIER = ROOT / "home/dot_claude/modify_private_settings.json"
HERDR_CONFIG = ROOT / "home/dot_config/herdr/config.toml"
FILE_VIEWER_CONFIG = ROOT / "home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml"
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
        self.pane_layout_path = self.temp_dir / "pane-layout.json"
        self.pane_layout_after_resize_path = self.temp_dir / "pane-layout-after-resize.json"
        self.pane_layout_exit_path = self.temp_dir / "pane-layout-exit.txt"
        self.agent_get_path = self.temp_dir / "agent-get.json"
        self.pane_counter_path = self.temp_dir / "pane-counter.txt"
        self.home_dir = self.temp_dir / "home"
        (self.home_dir / ".config/herdr").mkdir(parents=True)
        self.workdir = self.temp_dir / "project"
        self.workdir.mkdir()
        self.workspace_list_path.write_text('{"id":"cli:workspace:list","result":{"type":"workspace_list","workspaces":[]}}\n')
        self.pane_list_path.write_text('{"id":"cli:pane:list","result":{"panes":[]}}\n')
        self.pane_layout_path.write_text('{"id":"cli:pane:layout","result":{"layout":{"panes":[]}}}\n')
        self.pane_layout_after_resize_path.write_text("")
        self.pane_layout_exit_path.write_text("0\n")
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
if [[ $1 == pane && $2 == layout ]]; then
    cat {self.pane_layout_path}
    exit "$(cat {self.pane_layout_exit_path})"
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
if [[ $1 == pane && $2 == resize ]]; then
    if [[ -s {self.pane_layout_after_resize_path} ]]; then
        cp {self.pane_layout_after_resize_path} {self.pane_layout_path}
    fi
    exit 0
fi
if [[ $1 == pane && $2 == rename ]]; then
    printf '{{"id":"cli:pane:rename","result":{{"pane":{{"pane_id":"%s"}}}}}}\\n' "$3"
    exit 0
fi
if [[ $1 == pane && $2 == run ]]; then
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
        jq = shutil.which("jq")
        if jq is None:
            self.fail("jq is required for Herdr helper tests")
        (self.bin_dir / "jq").symlink_to(jq)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_executable(self, name: str, content: str) -> None:
        path = self.bin_dir / name
        path.write_text(textwrap.dedent(content))
        path.chmod(0o755)

    def install_agmsg_fakes(
        self,
        *,
        delivery_exit: int = 0,
        identities_output: str = "dotfiles-conformance\tcodex-worker",
        claude_identities_output: str = "dotfiles-conformance\tclaude-orchestrator",
    ) -> Path:
        scripts = self.home_dir / ".agents/skills/agmsg/scripts"
        scripts.mkdir(parents=True)
        delivery = scripts / "delivery.sh"
        delivery.write_text(
            f"""#!/usr/bin/env bash
printf 'delivery %s\\n' "$*" >> {self.calls_path}
exit {delivery_exit}
"""
        )
        delivery.chmod(0o755)
        codex_identities_output_path = scripts / "codex-identities-output.txt"
        codex_identities_output_path.write_text(identities_output)
        claude_identities_output_path = scripts / "claude-identities-output.txt"
        claude_identities_output_path.write_text(claude_identities_output)
        identities = scripts / "identities.sh"
        identities.write_text(
            f"""#!/usr/bin/env bash
printf 'identities %s\\n' "$*" >> {self.calls_path}
if [[ $2 == claude-code ]]; then
    cat {claude_identities_output_path}
else
    cat {codex_identities_output_path}
fi
"""
        )
        identities.chmod(0o755)
        return scripts

    def write_agmsg_turn_hook(self, scripts: Path) -> None:
        hooks = self.workdir / ".codex/hooks.json"
        hooks.parent.mkdir(exist_ok=True)
        hooks.write_text(
            json.dumps(
                {
                    "hooks": {
                        "Stop": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": f"'{scripts}/check-inbox.sh' 'codex' '{self.workdir}'",
                                    }
                                ],
                            }
                        ]
                    }
                }
            )
        )

    def write_agmsg_claude_hooks(self, scripts: Path) -> None:
        settings = self.workdir / ".claude/settings.local.json"
        settings.parent.mkdir(exist_ok=True)
        settings.write_text(
            json.dumps(
                {
                    "hooks": {
                        "SessionStart": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": (
                                            f"'{scripts}/session-start.sh' "
                                            f"'claude-code' '{self.workdir}'"
                                        ),
                                    }
                                ],
                            }
                        ]
                    }
                }
            )
        )

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
        pane_list = json.loads(f'{{"id":"cli:pane:list","result":{{"panes":[{panes}]}}}}')
        for pane in pane_list["result"]["panes"]:
            pane.setdefault("tab_id", f"{workspace_id}:t1")
        self.pane_list_path.write_text(json.dumps(pane_list) + "\n")
        if agent_pane_id:
            self.agent_get_path.write_text(f'{{"id":"cli:agent:get","result":{{"agent":{{"pane_id":"{agent_pane_id}"}},"type":"agent_info"}}}}\n')
        else:
            self.agent_get_path.write_text("")

    def write_pane_layout(self, panes: list[tuple[str, int]]) -> None:
        layout_panes = [
            {"pane_id": pane_id, "rect": {"height": 40, "width": 40, "x": x, "y": 0}}
            for pane_id, x in panes
        ]
        self.pane_layout_path.write_text(
            json.dumps({"id": "cli:pane:layout", "result": {"layout": {"panes": layout_panes}}}) + "\n"
        )

    def write_ratio_layout(
        self,
        widths: tuple[int, int],
        *,
        after_resize: bool = False,
        pane_ids: tuple[str, str] = ("w-attach:p1", "w-attach:p2"),
    ) -> None:
        left, right = widths
        left_id, right_id = pane_ids
        total = sum(widths)
        layout = {
            "id": "cli:pane:layout",
            "result": {
                "layout": {
                    "panes": [
                        {"pane_id": left_id, "rect": {"height": 40, "width": left, "x": 0, "y": 0}},
                        {
                            "pane_id": right_id,
                            "rect": {"height": 40, "width": right, "x": left, "y": 0},
                        },
                    ],
                    "splits": [
                        {"direction": "right", "rect": {"height": 40, "width": total, "x": 0, "y": 0}},
                    ],
                }
            },
        }
        path = self.pane_layout_after_resize_path if after_resize else self.pane_layout_path
        path.write_text(json.dumps(layout) + "\n")

    def run_helper(self) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(self.home_dir)
        env["PATH"] = f"{self.bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin"
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

    def run_attach_helper(
        self, *, in_herdr: bool, managed_layout: bool = False
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(self.home_dir)
        env["PATH"] = f"{self.bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin"
        for key in ("HERDR_ENV", "HERDR_PANE_ID", "HERDR_WORKSPACE_ID", "HERDR_AGENTS_LAYOUT"):
            env.pop(key, None)
        if in_herdr:
            env.update(
                HERDR_ENV="1",
                HERDR_PANE_ID="w-attach:p1",
                HERDR_WORKSPACE_ID="w-attach",
            )
        if managed_layout:
            env["HERDR_AGENTS_LAYOUT"] = "managed"
        return subprocess.run(
            ["bash", str(SCRIPT), "--attach"],
            cwd=self.workdir,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def run_agmsg_bootstrap_helper(self) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(self.home_dir)
        env["PATH"] = f"{self.bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin"
        return subprocess.run(
            ["bash", str(SCRIPT), "--bootstrap-agmsg", str(self.workdir)],
            cwd=ROOT,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_attach_noops_without_herdr_environment(self) -> None:
        result = self.run_attach_helper(in_herdr=False)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(self.calls_path.exists())

    def test_attach_noops_for_full_mode_managed_layout(self) -> None:
        result = self.run_attach_helper(in_herdr=True, managed_layout=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(self.calls_path.exists())

    def test_attach_builds_codex_right_of_current_claude_pane(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","pane_id":"w-attach:p1","workspace_id":"w-attach"}}',
        )

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        codex_start = next(call for call in calls if call.startswith("agent start codex-worker-w-attach "))
        self.assertIn("--split right", codex_start)
        self.assertIn("pane rename w-attach:p1 claude-orchestrator", calls)
        self.assertFalse(any(call.startswith("pane split ") for call in calls))
        self.assertFalse(any(call.startswith("pane run w-attach:p1 ") for call in calls))
        self.assertFalse(any(call.startswith("workspace create ") for call in calls))

    def test_attach_complete_workspace_is_idempotent(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_ratio_layout((60, 60))

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertFalse(any(call.startswith(("agent start ", "pane rename ", "pane run ", "pane split ")) for call in calls))

    def test_attach_repairs_codex_claude_order_with_one_swap(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_pane_layout([("w-attach:p2", 0), ("w-attach:p1", 40)])

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        swaps = [
            call
            for call in self.calls_path.read_text().splitlines()
            if call.startswith("pane swap ")
        ]
        self.assertEqual(
            swaps,
            ["pane swap --source-pane w-attach:p2 --target-pane w-attach:p1"],
        )

    def test_attach_correct_order_does_not_swap(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_pane_layout([("w-attach:p1", 0), ("w-attach:p2", 40)])

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(
            any(
                call.startswith("pane swap ")
                for call in self.calls_path.read_text().splitlines()
            )
        )

    def test_attach_equal_halves_does_not_resize(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_ratio_layout((60, 60))

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(
            any(
                call.startswith("pane resize ")
                for call in self.calls_path.read_text().splitlines()
            )
        )

    def test_attach_repairs_skewed_widths_to_equal_halves(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_ratio_layout((90, 30))
        self.write_ratio_layout((60, 60), after_resize=True)

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        resize_calls = [
            call
            for call in self.calls_path.read_text().splitlines()
            if call.startswith("pane resize ")
        ]
        self.assertEqual(len(resize_calls), 1)
        self.assertRegex(
            resize_calls[0],
            r"^pane resize --pane w-attach:p1 --direction left --amount 0\.25",
        )
        widths = [
            pane["rect"]["width"]
            for pane in json.loads(self.pane_layout_path.read_text())["result"]["layout"]["panes"]
        ]
        self.assertLessEqual(max(widths) - min(widths), 2)

    def test_attach_warns_after_one_nonconverging_resize(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_ratio_layout((90, 30))

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("did not converge", result.stderr)
        self.assertEqual(
            len(
                [
                    call
                    for call in self.calls_path.read_text().splitlines()
                    if call.startswith("pane resize ")
                ]
            ),
            1,
        )

    def test_attach_ratio_repair_skips_unsafe_layouts(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        cases = (
            ('{"result":{"layout":{"panes":[]}}}\n', 42),
            (
                '{"result":{"layout":{"panes":['
                '{"pane_id":"w-attach:p1","rect":{"x":0,"width":"wide"}},'
                '{"pane_id":"w-attach:p2","rect":{"x":40,"width":40}}'
                ']}}}\n',
                0,
            ),
            (
                '{"result":{"layout":{"panes":['
                '{"pane_id":"w-attach:p1","rect":{"x":0,"width":40}},'
                '{"pane_id":"w-attach:p2","rect":{"x":40,"width":40}}'
                '],"splits":[]}}}\n',
                0,
            ),
        )
        for payload, exit_code in cases:
            with self.subTest(exit_code=exit_code, payload=payload):
                self.calls_path.write_text("")
                self.pane_layout_path.write_text(payload)
                self.pane_layout_exit_path.write_text(f"{exit_code}\n")

                result = self.run_attach_helper(in_herdr=True)

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("refusing ratio repair", result.stderr.lower())
                self.assertFalse(
                    any(
                        call.startswith("pane resize ")
                        for call in self.calls_path.read_text().splitlines()
                    )
                )

    def test_attach_legacy_files_pane_refuses_repair_without_layout_mutation(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}},'
            f'{{"agent":null,"cwd":"{self.workdir}","label":"files","pane_id":"w-attach:p9","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ambiguous", result.stderr.lower())
        mutations = [
            call
            for call in self.calls_path.read_text().splitlines()
            if call.startswith(("agent start ", "pane rename ", "pane run ", "pane split ", "pane swap ", "pane resize "))
        ]
        self.assertEqual(mutations, ["pane rename w-attach:p1 claude-orchestrator"])

    def test_attach_ignores_extra_panes_on_other_tabs(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}},'
            f'{{"agent":null,"cwd":"{self.workdir}","pane_id":"w-attach:p3","tab_id":"w-attach:t2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_ratio_layout((60, 60))

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertIn("pane rename w-attach:p1 claude-orchestrator", calls)
        self.assertFalse(any(call.startswith("pane swap ") for call in calls))
        self.assertFalse(any("w-attach:p3" in call for call in calls))

    def test_attach_does_not_restart_codex_agent_from_another_tab(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","tab_id":"w-attach:t2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("another Herdr tab", result.stderr)
        self.assertFalse(
            any(
                call.startswith("agent start ")
                for call in self.calls_path.read_text().splitlines()
            )
        )

    def test_attach_bootstraps_agmsg_after_codex_reuse(self) -> None:
        self.install_agmsg_fakes()
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_ratio_layout((60, 60))

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertIn(f"delivery set turn codex {self.workdir.resolve()}", calls)
        self.assertIn(f"identities {self.workdir.resolve()} codex", calls)

    def test_attach_bootstraps_agmsg_after_codex_start(self) -> None:
        self.install_agmsg_fakes()
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","pane_id":"w-attach:p1","workspace_id":"w-attach"}}',
        )

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertIn(f"delivery set turn codex {self.workdir.resolve()}", calls)
        self.assertIn(f"identities {self.workdir.resolve()} codex", calls)
        self.assertIn("/hooks", result.stderr)
        self.assertIn("trust", result.stderr.lower())

    def test_attach_skips_delivery_when_turn_hook_exists(self) -> None:
        scripts = self.install_agmsg_fakes()
        self.write_agmsg_turn_hook(scripts)
        self.write_agmsg_claude_hooks(scripts)
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_ratio_layout((60, 60))

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertFalse(any(call.startswith("delivery ") for call in calls))
        self.assertIn(f"identities {self.workdir.resolve()} codex", calls)
        self.assertIn(f"identities {self.workdir.resolve()} claude-code", calls)

    def test_attach_warns_when_multiple_agmsg_identities_exist(self) -> None:
        scripts = self.install_agmsg_fakes(
            identities_output=(
                "dotfiles-conformance\tcodex-worker-a\n"
                "dotfiles-conformance\tcodex-worker-b"
            )
        )
        self.write_agmsg_turn_hook(scripts)
        self.write_agmsg_claude_hooks(scripts)
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-attach:p1","workspace_id":"w-attach"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-attach:p2","workspace_id":"w-attach"}}',
            agent_pane_id="w-attach:p2",
        )
        self.write_ratio_layout((60, 60))

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Multiple agmsg Codex identities", result.stderr)
        self.assertFalse(
            any(
                call.startswith("delivery ")
                for call in self.calls_path.read_text().splitlines()
            )
        )

    def test_full_mode_skips_agmsg_bootstrap_for_home(self) -> None:
        self.install_agmsg_fakes()
        self.workdir = self.home_dir

        result = self.run_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Skipping agmsg bootstrap for $HOME", result.stderr)
        calls = self.calls_path.read_text().splitlines() if self.calls_path.exists() else []
        self.assertFalse(
            any(
                call.startswith(("delivery ", "identities "))
                for call in calls
            )
        )

    def test_attach_reports_agmsg_skip_when_not_installed(self) -> None:
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","pane_id":"w-attach:p1","workspace_id":"w-attach"}}',
        )

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("agmsg delivery script not found; skipping bootstrap", result.stderr)

    def test_attach_ignores_agmsg_bootstrap_failure(self) -> None:
        self.install_agmsg_fakes(delivery_exit=42, identities_output="")
        self.write_workspace_state(
            "w-attach",
            f'{{"agent":"claude","cwd":"{self.workdir}","pane_id":"w-attach:p1","workspace_id":"w-attach"}}',
        )

        result = self.run_attach_helper(in_herdr=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bootstrap_only_skips_all_delivery_when_both_hooks_exist(self) -> None:
        scripts = self.install_agmsg_fakes()
        self.write_agmsg_turn_hook(scripts)
        self.write_agmsg_claude_hooks(scripts)

        result = self.run_agmsg_bootstrap_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertFalse(any(call.startswith("delivery ") for call in calls))
        self.assertEqual(
            [call for call in calls if call.startswith("identities ")],
            [
                f"identities {self.workdir.resolve()} codex",
                f"identities {self.workdir.resolve()} claude-code",
            ],
        )

    def test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing(self) -> None:
        scripts = self.install_agmsg_fakes()
        self.write_agmsg_turn_hook(scripts)

        result = self.run_agmsg_bootstrap_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertEqual(
            [call for call in calls if call.startswith("delivery ")],
            [f"delivery set both claude-code {self.workdir.resolve()}"],
        )
        self.assertIn("next Claude Code session", result.stderr)

    def test_bootstrap_only_sets_each_missing_delivery_once(self) -> None:
        self.install_agmsg_fakes()

        result = self.run_agmsg_bootstrap_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertEqual(
            [call for call in calls if call.startswith("delivery ")],
            [
                f"delivery set turn codex {self.workdir.resolve()}",
                f"delivery set both claude-code {self.workdir.resolve()}",
            ],
        )

    def test_bootstrap_only_creates_missing_herdr_log_directory(self) -> None:
        self.install_agmsg_fakes()
        shutil.rmtree(self.home_dir / ".config/herdr")

        result = self.run_agmsg_bootstrap_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.home_dir / ".config/herdr").is_dir())

    def test_bootstrap_only_warns_for_missing_claude_identity_without_joining(self) -> None:
        scripts = self.install_agmsg_fakes(claude_identities_output="")
        self.write_agmsg_turn_hook(scripts)
        self.write_agmsg_claude_hooks(scripts)

        result = self.run_agmsg_bootstrap_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("No agmsg Claude Code identity", result.stderr)
        self.assertIn("join.sh <team> <agent-name> claude-code", result.stderr)
        self.assertFalse(
            any(call.startswith("join ") for call in self.calls_path.read_text().splitlines())
        )

    def test_bootstrap_only_warns_for_multiple_claude_identities(self) -> None:
        scripts = self.install_agmsg_fakes(
            claude_identities_output=(
                "dotfiles-conformance\tclaude-a\n"
                "dotfiles-conformance\tclaude-b"
            )
        )
        self.write_agmsg_turn_hook(scripts)
        self.write_agmsg_claude_hooks(scripts)

        result = self.run_agmsg_bootstrap_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Multiple agmsg Claude Code identities", result.stderr)
        self.assertFalse(
            any(call.startswith("join ") for call in self.calls_path.read_text().splitlines())
        )

    def test_bootstrap_only_does_not_call_herdr_or_agents(self) -> None:
        scripts = self.install_agmsg_fakes()
        self.write_agmsg_turn_hook(scripts)
        self.write_agmsg_claude_hooks(scripts)

        result = self.run_agmsg_bootstrap_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertFalse(
            any(
                call.startswith(("workspace ", "pane ", "agent "))
                for call in calls
            )
        )

    def test_bootstrap_only_skips_home_without_agmsg_calls(self) -> None:
        self.install_agmsg_fakes()
        self.workdir = self.home_dir

        result = self.run_agmsg_bootstrap_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Skipping agmsg bootstrap for $HOME", result.stderr)
        calls = self.calls_path.read_text().splitlines() if self.calls_path.exists() else []
        self.assertFalse(
            any(
                call.startswith(("delivery ", "identities "))
                for call in calls
            )
        )

    def test_make_update_and_upgrade_include_agmsg_bootstrap(self) -> None:
        for target in ("update", "upgrade"):
            with self.subTest(target=target):
                result = subprocess.run(
                    ["make", "-n", "-f", str(MAKEFILE), target],
                    cwd=ROOT,
                    check=False,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("make agmsg-bootstrap", result.stdout)

    def test_claude_settings_add_herdr_attach_session_hook(self) -> None:
        source_dir = self.temp_dir / "source"
        (source_dir / ".chezmoitemplates").mkdir(parents=True)
        (source_dir / ".chezmoitemplates/claude-settings-managed.json").write_text(
            '{"enabledPlugins": {}, "hooks": {"SessionStart": []}}\n'
        )
        env = os.environ.copy()
        env["CHEZMOI_SOURCE_DIR"] = str(source_dir)
        env["CHEZMOI_HOME_DIR"] = str(self.home_dir)

        result = subprocess.run(
            [sys.executable, str(CLAUDE_SETTINGS_MODIFIER)],
            input="",
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        session_hooks = json.loads(result.stdout)["hooks"]["SessionStart"]
        command = session_hooks[-1]["hooks"][0]["command"]
        self.assertIn("herdr-agents --attach", command)
        self.assertIn("herdr-agents.log", command)
        self.assertTrue(command.endswith("|| true"))

    def test_herdr_session_does_not_prebuild_agent_layout(self) -> None:
        self.assertNotIn("herdr-agents", HERDR_SESSION_SCRIPT.read_text())

    def test_uses_initial_workspace_pane_for_claude_and_splits_codex_right(self) -> None:
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        calls = self.calls_path.read_text().splitlines()
        self.assertIn("pane rename w-test:p1 claude-orchestrator", calls)
        self.assertIn("pane run w-test:p1 CLICOLOR_FORCE=1 FORCE_COLOR=1 HERDR_AGENTS_LAYOUT=managed claude", calls)
        self.assertIn(
            f"agent start codex-worker-w-test --cwd {self.workdir} --workspace w-test --split right --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- {self.bin_dir}/codex --sandbox workspace-write --profile standard",
            calls,
        )
        self.assertIn("pane rename w-test:p2 codex-worker", calls)
        self.assertFalse(any(call.startswith("pane split ") for call in calls))
        self.assertNotIn(
            f"agent start claude --cwd {self.workdir} --workspace w-test --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --focus -- claude",
            calls,
        )

    def install_npm_fake(self, *, installed: bool, mise_has_tool: bool = True) -> None:
        list_exit = 0 if installed else 1
        where_exit = 0 if mise_has_tool else 1
        self.write_executable(
            "npm",
            f"""#!/usr/bin/env bash
printf 'npm %s\\n' "$*" >> {self.calls_path}
if [[ $1 == list ]]; then
    exit {list_exit}
fi
""",
        )
        self.write_executable(
            "mise",
            f"""#!/usr/bin/env bash
if [[ $1 == where ]]; then
    exit {where_exit}
fi
""",
        )

    def test_start_removes_node_global_agent_clis_shadowing_mise(self) -> None:
        self.install_npm_fake(installed=True)

        result = self.run_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertIn("npm uninstall -g @openai/codex", calls)
        self.assertIn("npm uninstall -g @anthropic-ai/claude-code", calls)

    def test_start_skips_node_global_removal_without_stray(self) -> None:
        self.install_npm_fake(installed=False)

        result = self.run_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertFalse(any(call.startswith("npm uninstall") for call in calls))

    def test_start_keeps_node_global_without_mise_tool_install(self) -> None:
        self.install_npm_fake(installed=True, mise_has_tool=False)

        result = self.run_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertFalse(any(call.startswith("npm uninstall") for call in calls))

    def test_existing_two_pane_workspace_repairs_skewed_widths(self) -> None:
        self.write_workspace_state(
            "w-old",
            f'{{"agent":"claude","cwd":"{self.workdir}","label":"claude-orchestrator","pane_id":"w-old:p1","workspace_id":"w-old"}},'
            f'{{"agent":"codex","cwd":"{self.workdir}","label":"codex-worker","pane_id":"w-old:p2","workspace_id":"w-old"}}',
            agent_pane_id="w-old:p2",
        )
        self.write_ratio_layout((90, 30), pane_ids=("w-old:p1", "w-old:p2"))
        self.write_ratio_layout(
            (60, 60), after_resize=True, pane_ids=("w-old:p1", "w-old:p2")
        )

        result = self.run_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertEqual(
            [call for call in calls if call.startswith("pane resize ")],
            ["pane resize --pane w-old:p1 --direction left --amount 0.25"],
        )
        self.assertIn("workspace focus w-old", calls)

    def test_existing_workspace_with_legacy_files_pane_focuses_without_mutation(self) -> None:
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
        self.assertFalse(any(call.startswith("pane run w-old:p9 ") for call in calls))

    def test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again(self) -> None:
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
        self.assertIn("pane run w-old:p3 CLICOLOR_FORCE=1 FORCE_COLOR=1 HERDR_AGENTS_LAYOUT=managed claude", calls)
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
            f"agent start codex-worker-w-old --cwd {self.workdir} --workspace w-old --split right --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- {self.bin_dir}/codex --sandbox workspace-write --profile standard",
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
            f"agent start codex-worker-w-old --cwd {self.workdir} --workspace w-old --split right --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- {self.bin_dir}/codex --sandbox workspace-write --profile standard",
            calls,
        )
        self.assertIn("pane run w-old:p3 CLICOLOR_FORCE=1 FORCE_COLOR=1 HERDR_AGENTS_LAYOUT=managed claude", calls)
        self.assertNotIn("pane run w-old:p2 CLICOLOR_FORCE=1 FORCE_COLOR=1 HERDR_AGENTS_LAYOUT=managed claude", calls)

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
        self.assertIn("pane run w-old:p1 CLICOLOR_FORCE=1 FORCE_COLOR=1 HERDR_AGENTS_LAYOUT=managed claude", calls)
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
        self.assertIn("pane run w-old:p3 CLICOLOR_FORCE=1 FORCE_COLOR=1 HERDR_AGENTS_LAYOUT=managed claude", calls)
        self.assertIn("workspace focus w-old", calls)

    def test_ghostty_herdr_starts_plain_workspace(self) -> None:
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
                "herdr ",
            ],
        )
        e2e_lines = e2e_log.read_text()
        self.assertIn(f"attached workspace from cwd={self.workdir.resolve()}", e2e_lines)
        self.assertNotIn("claude cwd=", e2e_lines)
        self.assertNotIn("codex cwd=", e2e_lines)

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

    def test_herdr_session_execs_herdr_without_prebuilding_agents(self) -> None:
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
            ["herdr "],
        )
        self.assertFalse((self.home_dir / ".config/herdr/herdr-agents.log").exists())

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

    def test_herdr_prefix_f_opens_file_viewer_popup(self) -> None:
        config = tomllib.loads(HERDR_CONFIG.read_text())
        command = next(item for item in config["keys"]["command"] if item["key"] == "prefix+f")

        self.assertEqual(command["type"], "popup")
        self.assertEqual(command["width"], "90%")
        self.assertEqual(command["height"], "90%")
        self.assertIn("herdr-file-viewer", command["command"])
        self.assertIn("HERDR_PLUGIN_CONFIG_DIR", command["command"])

    def test_file_viewer_plugin_config_sets_micro_editor(self) -> None:
        config = tomllib.loads(FILE_VIEWER_CONFIG.read_text())

        self.assertEqual(config, {"editor": "micro"})

    def test_yazi_edit_opener_prefers_zed_with_editor_fallback(self) -> None:
        config = tomllib.loads(YAZI_CONFIG.read_text())

        self.assertEqual(
            config["opener"]["edit"],
            [
                {
                    "run": "command -v zed >/dev/null && zed --add %s || ${EDITOR:-vi} %s",
                    "block": True,
                    "for": "unix",
                }
            ],
        )

        editor_calls = self.temp_dir / "editor-calls.txt"
        self.write_executable("editor", f'#!/usr/bin/env bash\nprintf "%s\\n" "$*" > {editor_calls}\n')
        env = {"PATH": f"{self.bin_dir}:/usr/bin:/bin", "EDITOR": "editor"}
        result = subprocess.run(
            ["bash", "-c", config["opener"]["edit"][0]["run"].replace("%s", "example.txt")],
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(editor_calls.read_text(), "example.txt\n")

        zed_calls = self.temp_dir / "zed-calls.txt"
        self.write_executable("zed", f'#!/usr/bin/env bash\nprintf "%s\\n" "$*" > {zed_calls}\n')
        editor_calls.unlink()
        result = subprocess.run(
            ["bash", "-c", config["opener"]["edit"][0]["run"].replace("%s", "example.txt")],
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(zed_calls.read_text(), "--add example.txt\n")
        self.assertFalse(editor_calls.exists())

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

    def test_bare_herdr_in_ghostty_starts_plain_session(self) -> None:
        result = self.run_zshrc_herdr("herdr", ghostty=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls_path.read_text().splitlines(),
            ["herdr-session "],
        )

    def test_interactive_ghostty_shell_attaches_plain_session(self) -> None:
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
