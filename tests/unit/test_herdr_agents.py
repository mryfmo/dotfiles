#!/usr/bin/env python3
"""Exercise the Herdr agent workspace helper with fake CLIs."""

from __future__ import annotations

import json
import os
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
        self.agent_start_failures_path = self.temp_dir / "agent-start-failures.txt"
        self.agent_start_not_ready_path = self.temp_dir / "agent-start-not-ready.txt"
        # 1 makes the next agent start fail with agent_name_taken.
        self.agent_start_name_taken_path = self.temp_dir / "agent-start-name-taken.txt"
        # agent list polls that still show the taken name; -1 means forever.
        self.agent_list_taken_polls_path = self.temp_dir / "agent-list-taken-polls.txt"
        self.agent_taken_name_path = self.temp_dir / "agent-taken-name.txt"
        self.trust_dialog_match_path = self.temp_dir / "trust-dialog-match.txt"
        # shell, shell-pid (a non-sh name that is the pane's shell_pid),
        # exit-dialog (claude foreground until an Enter), stuck, or unavailable.
        self.process_info_state_path = self.temp_dir / "process-info-state.txt"
        self.orchestrator_session_path = self.temp_dir / "orchestrator-session.txt"
        # 1 makes the visible snapshot stale: it shows old transcript text and
        # a prompt wait on it times out, as for a background tab.
        self.visible_stale_path = self.temp_dir / "visible-stale.txt"
        # The recent-unwrapped snapshot text.
        self.recent_text_path = self.temp_dir / "recent-text.txt"
        self.pane_counter_path = self.temp_dir / "pane-counter.txt"
        self.tab_list_path = self.temp_dir / "tab-list.json"
        # Exit code the fake audit pane reports in its AUDIT-EXIT marker.
        self.audit_exit_path = self.temp_dir / "audit-exit.txt"
        self.home_dir = self.temp_dir / "home"
        (self.home_dir / ".config/herdr").mkdir(parents=True)
        self.workdir = self.temp_dir / "project"
        self.workdir.mkdir()
        self.workspace_list_path.write_text(
            '{"id":"cli:workspace:list","result":{"type":"workspace_list","workspaces":[]}}\n'
        )
        self.pane_list_path.write_text('{"id":"cli:pane:list","result":{"panes":[]}}\n')
        self.pane_layout_path.write_text('{"id":"cli:pane:layout","result":{"layout":{"panes":[]}}}\n')
        self.pane_layout_after_resize_path.write_text("")
        self.pane_layout_exit_path.write_text("0\n")
        self.agent_get_path.write_text("")
        self.agent_start_failures_path.write_text("0\n")
        self.agent_start_not_ready_path.write_text("0\n")
        self.agent_start_name_taken_path.write_text("0\n")
        self.agent_list_taken_polls_path.write_text("0\n")
        self.trust_dialog_match_path.write_text("0\n")
        self.process_info_state_path.write_text("shell\n")
        self.visible_stale_path.write_text("0\n")
        self.recent_text_path.write_text("~/project \u276f \n\n\n")
        self.pane_counter_path.write_text("2\n")
        self.tab_list_path.write_text('{"id":"cli:tab:list","result":{"tabs":[]}}\n')
        self.audit_exit_path.write_text("0\n")

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
if [[ $1 == tab && $2 == list ]]; then
    cat {self.tab_list_path}
    exit 0
fi
if [[ $1 == tab && $2 == create ]]; then
    workspace="$4"
    cwd="$6"
    jq -c --arg ws "$workspace" '.result.tabs += [{{"label":"audit","tab_id":($ws + ":t2"),"workspace_id":$ws}}]' {self.tab_list_path} > {self.tab_list_path}.new
    mv {self.tab_list_path}.new {self.tab_list_path}
    jq -c --arg ws "$workspace" --arg cwd "$cwd" '.result.panes += [{{"agent":null,"cwd":$cwd,"pane_id":($ws + ":p9"),"tab_id":($ws + ":t2"),"workspace_id":$ws}}]' {self.pane_list_path} > {self.pane_list_path}.new
    mv {self.pane_list_path}.new {self.pane_list_path}
    printf '%s\\n' '{{"id":"cli:tab:create","result":{{}}}}'
    exit 0
fi
if [[ $1 == pane && $2 == read ]]; then
    case " $* " in
    *" --source visible "*) [[ $(cat {self.visible_stale_path}) == 1 ]] && printf 'stale audit transcript line\\n' ;;
    *" --source recent-unwrapped "*) cat {self.recent_text_path} ;;
    esac
    exit 0
fi
if [[ $1 == pane && $2 == wait-output ]]; then
    if [[ " $* " == *" --source visible "* && $(cat {self.visible_stale_path}) == 1 ]]; then
        exit 1
    fi
    for arg in "$@"; do
        if [[ $arg == AUDIT-EXIT-*':[0-9]+' ]]; then
            printf '{{"id":"cli:pane:wait-output","result":{{"matched_line":"%s:%s"}}}}\\n' "${{arg%':[0-9]+'}}" "$(cat {self.audit_exit_path})"
            exit 0
        fi
        if [[ $arg == "trust this folder" ]]; then
            [[ $(cat {self.trust_dialog_match_path}) == 1 ]] && exit 0
            exit 1
        fi
    done
    exit 0
fi
if [[ $1 == pane && $2 == process-info ]]; then
    if [[ ${{4:-}} == w-test:p1 && -s {self.orchestrator_session_path} ]] &&
        grep -q '^agent start claude-orchestrator' {self.calls_path}; then
        printf '%s\\n' '{{"id":"cli:pane:process_info","result":{{"process_info":{{"foreground_processes":[{{"argv":["claude"],"cmdline":"claude","name":"claude","pid":4343}}],"pane_id":"w-test:p1"}}}}}}'
        exit 0
    fi
    state="$(cat {self.process_info_state_path})"
    if [[ $state == unavailable ]]; then
        exit 1
    fi
    if [[ $state == shell-pid ]]; then
        printf '%s\\n' '{{"id":"cli:pane:process_info","result":{{"process_info":{{"shell_pid":4242,"foreground_processes":[{{"argv":["nu"],"cmdline":"nu","name":"nu","pid":4242}}]}}}}}}'
        exit 0
    fi
    if [[ $state != shell ]]; then
        printf '%s\\n' '{{"id":"cli:pane:process_info","result":{{"process_info":{{"foreground_processes":[{{"argv":["claude"],"cmdline":"claude","name":"claude","pid":4343}}]}}}}}}'
        exit 0
    fi
    printf '%s\\n' '{{"id":"cli:pane:process_info","result":{{"process_info":{{"foreground_processes":[{{"argv":["/bin/zsh"],"cmdline":"/bin/zsh","name":"zsh","pid":4242}}]}}}}}}'
    exit 0
fi
if [[ $1 == agent && $2 == send-keys && ${{@: -1}} == Enter ]]; then
    if [[ $(cat {self.process_info_state_path}) == exit-dialog ]]; then
        printf 'shell\\n' > {self.process_info_state_path}
    fi
    exit 0
fi
if [[ $1 == agent && $2 == start ]]; then
    name="$3"
    kind=''
    pane=''
    shift 3
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --kind) kind="$2"; shift 2 ;;
            --pane) pane="$2"; shift 2 ;;
            --cwd|--workspace|--split|--env|--focus|--no-focus)
                printf 'removed agent start option: %s\\n' "$1" >&2
                exit 64
                ;;
            --) shift; break ;;
            *) shift ;;
        esac
    done
    if [[ ! $name =~ ^[a-z][a-z0-9_-]{{0,31}}$ ]]; then
        printf 'invalid_agent_name: %s\\n' "$name" >&2
        exit 64
    fi
    if [[ $kind != codex && $kind != claude ]] || [[ -z $pane ]]; then
        printf 'agent start requires --kind and --pane\\n' >&2
        exit 64
    fi
    failures="$(cat {self.agent_start_failures_path})"
    if (( failures > 0 )); then
        printf '%s\\n' "$(( failures - 1 ))" > {self.agent_start_failures_path}
        printf 'agent start timeout\\n' >&2
        exit 1
    fi
    if [[ $(cat {self.agent_start_name_taken_path}) == 1 ]]; then
        printf '0\\n' > {self.agent_start_name_taken_path}
        printf '%s\\n' "$name" > {self.agent_taken_name_path}
        printf 'agent_name_taken: %s\\n' "$name" >&2
        exit 1
    fi
    if [[ $(cat {self.agent_start_not_ready_path}) == 1 ]]; then
        printf '0\\n' > {self.agent_start_not_ready_path}
        printf 'agent_not_ready\\n' >&2
        exit 1
    fi
    printf '{{"id":"cli:agent:start","result":{{"pane":{{"pane_id":"%s"}}}}}}\\n' "$pane"
    exit 0
fi
if [[ $1 == agent && $2 == list ]]; then
    polls="$(cat {self.agent_list_taken_polls_path})"
    if (( polls != 0 )); then
        (( polls > 0 )) && printf '%s\\n' "$(( polls - 1 ))" > {self.agent_list_taken_polls_path}
        printf '{{"id":"cli:agent:list","result":{{"agents":[{{"name":"%s","agent_status":"idle"}},{{"agent_status":"idle"}}]}}}}\\n' "$(cat {self.agent_taken_name_path})"
        exit 0
    fi
    if [[ -s {self.orchestrator_session_path} ]]; then
        sid="$(cat {self.orchestrator_session_path})"
        printf '{{"id":"cli:agent:list","result":{{"agents":[{{"agent":"claude","pane_id":"w-test:p1","agent_session":{{"value":"%s"}},"agent_status":"idle"}},{{"agent":"claude","pane_id":"w-attach:p1","agent_session":{{"value":"%s"}},"agent_status":"idle"}}]}}}}\\n' "$sid" "$sid"
        exit 0
    fi
    printf '%s\\n' '{{"id":"cli:agent:list","result":{{"agents":[{{"agent_status":"idle"}}]}}}}'
    exit 0
fi
if [[ $1 == agent && $2 == wait ]]; then
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
        doctor = scripts / "doctor.sh"
        doctor.write_text(
            f"""#!/usr/bin/env bash
printf 'doctor %s\\n' "$*" >> {self.calls_path}
type=""
while [[ $# -gt 0 ]]; do
    case "$1" in
    --type) type="$2"; shift 2 ;;
    *) shift ;;
    esac
done
if [[ $type == claude-code ]]; then
    output_file={claude_identities_output_path}
else
    output_file={codex_identities_output_path}
fi
if [[ -s "$output_file" ]]; then
    printf '1 team(s), 1 registration(s), 0 warning(s)\\n'
    exit 0
else
    printf 'doctor: no registrations match this scope\\n' >&2
    exit 2
fi
"""
        )
        doctor.chmod(0o755)
        return scripts

    def run_agmsg_retire_helper(
        self, *mode: str, extra_env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(self.home_dir)
        env["PATH"] = f"{self.bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin"
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            ["bash", str(SCRIPT), *(mode or ("--retire-agmsg",)), str(self.workdir)],
            cwd=ROOT,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def install_agmsg_retire_fakes(self, *, strip_hooks: bool = True) -> Path:
        """agmsg fakes for --retire-agmsg: `set off` strips the hooks, leave drops the identity."""
        scripts = self.install_agmsg_fakes()
        settings = self.workdir / ".claude/settings.local.json"
        strip = f"jq 'del(.hooks)' {settings} > {settings}.new && mv {settings}.new {settings}\n" if strip_hooks else ""
        (scripts / "delivery.sh").write_text(
            f"#!/usr/bin/env bash\nprintf 'delivery %s\\n' \"$*\" >> {self.calls_path}\n{strip}"
        )
        (scripts / "leave.sh").write_text(
            f"#!/usr/bin/env bash\nprintf 'leave %s\\n' \"$*\" >> {self.calls_path}\n"
            f": > {scripts / 'claude-identities-output.txt'}\n"
        )
        (scripts / "leave.sh").chmod(0o755)
        team = self.home_dir / ".agents/skills/agmsg/teams/dotfiles-conformance"
        team.mkdir(parents=True)
        (team / "config.json").write_text('{"name": "dotfiles-conformance", "agents": {}}')
        settings.parent.mkdir(exist_ok=True)
        hooks = {
            event: [
                {
                    "matcher": "",
                    "hooks": [{"type": "command", "command": f"'{scripts}/{hook}' 'claude-code' '{self.workdir}'"}],
                }
            ]
            for event, hook in (
                ("SessionStart", "session-start.sh"),
                ("SessionEnd", "session-end.sh"),
                ("Stop", "check-inbox.sh"),
            )
        }
        settings.write_text(
            json.dumps(
                {
                    "permissions": {
                        "allow": ["Bash(git status:*)", f"Bash({scripts}/inbox.sh dotfiles-conformance *)"]
                    },
                    "hooks": hooks,
                }
            )
        )
        return scripts

    def test_retire_agmsg_removes_the_hooks_then_leaves_and_a_second_run_does_nothing(self) -> None:
        scripts = self.install_agmsg_retire_fakes()
        settings = self.workdir.resolve() / ".claude/settings.local.json"

        result = self.run_agmsg_retire_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            [c for c in self.calls_path.read_text().splitlines() if c.startswith(("delivery ", "leave "))],
            [
                f"delivery set off claude-code {self.workdir.resolve()}",
                "leave dotfiles-conformance claude-orchestrator",
            ],
        )
        self.assertEqual(
            result.stdout,
            f"agmsg retired: removed the agmsg hooks from {settings}\n"
            f"agmsg retired: {settings} keeps the allow rule Bash({scripts}/inbox.sh dotfiles-conformance *)"
            " (delivery.sh set off leaves permissions alone)\n"
            "agmsg retired: claude-orchestrator left team dotfiles-conformance\n",
        )
        self.assertNotIn("hooks", json.loads(settings.read_text()))

        self.calls_path.unlink()
        again = self.run_agmsg_retire_helper()

        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertEqual(again.stdout, f"agmsg already retired for {self.workdir.resolve()}\n")
        self.assertFalse(
            any(c.startswith(("delivery ", "leave ")) for c in self.calls_path.read_text().splitlines()),
            self.calls_path.read_text(),
        )

    def test_retire_agmsg_fails_when_a_hook_survives_set_off(self) -> None:
        self.install_agmsg_retire_fakes(strip_hooks=False)
        settings = self.workdir.resolve() / ".claude/settings.local.json"

        result = self.run_agmsg_retire_helper()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"agmsg hooks remain in {settings} after delivery.sh set off claude-code", result.stderr)
        self.assertNotIn("agmsg retired", result.stdout)
        # The identity stays until its hooks are gone.
        self.assertFalse(any(c.startswith("leave ") for c in self.calls_path.read_text().splitlines()))

    def test_retire_agmsg_fails_naming_a_settings_file_it_cannot_read_before_set_off(self) -> None:
        self.install_agmsg_retire_fakes()
        settings = self.workdir.resolve() / ".claude/settings.local.json"
        for name, content in (("malformed", '{"hooks": {'), ("empty", "")):
            with self.subTest(settings=name):
                settings.write_text(content)
                self.calls_path.unlink(missing_ok=True)

                result = self.run_agmsg_retire_helper()

                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(f"cannot read {settings} as JSON before delivery.sh set off", result.stderr)
                self.assertEqual(result.stdout, "")
                calls = self.calls_path.read_text().splitlines() if self.calls_path.exists() else []
                self.assertFalse(any(c.startswith(("delivery ", "leave ")) for c in calls), calls)

    def test_retire_agmsg_fails_naming_a_settings_file_set_off_left_unreadable(self) -> None:
        scripts = self.install_agmsg_retire_fakes()
        settings = self.workdir.resolve() / ".claude/settings.local.json"
        (scripts / "delivery.sh").write_text(
            f"#!/usr/bin/env bash\nprintf 'delivery %s\\n' \"$*\" >> {self.calls_path}\nprintf '{{\"hooks\": ' > {settings}\n"
        )

        result = self.run_agmsg_retire_helper()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"cannot read {settings} as JSON after delivery.sh set off", result.stderr)
        self.assertNotIn("agmsg retired", result.stdout)
        calls = self.calls_path.read_text().splitlines()
        self.assertIn(f"delivery set off claude-code {self.workdir.resolve()}", calls)
        self.assertFalse(any(c.startswith("leave ") for c in calls), calls)

    def test_retire_agmsg_reports_a_missing_delivery_script_and_still_leaves(self) -> None:
        scripts = self.install_agmsg_retire_fakes()
        (scripts / "delivery.sh").unlink()

        result = self.run_agmsg_retire_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"agmsg delivery script not found; skipping hook removal: {scripts}/delivery.sh", result.stderr)
        self.assertEqual(result.stdout, "agmsg retired: claude-orchestrator left team dotfiles-conformance\n")

    def test_retire_agmsg_never_claims_retired_when_the_identity_lookup_fails(self) -> None:
        scripts = self.install_agmsg_retire_fakes()
        (self.workdir / ".claude/settings.local.json").write_text("{}")
        identities = scripts / "identities.sh"

        identities.write_text("#!/usr/bin/env bash\nprintf 'agmsg state unreadable\\n' >&2\nexit 3\n")
        result = self.run_agmsg_retire_helper()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"identities.sh {self.workdir.resolve()} claude-code failed", result.stderr)
        self.assertNotIn("already retired", result.stdout)

        identities.unlink()
        result = self.run_agmsg_retire_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"agmsg identities script not found; skipping team leave: {identities}", result.stderr)
        self.assertNotIn("already retired", result.stdout)

    def test_retire_agmsg_refuses_home_without_agmsg_calls(self) -> None:
        self.install_agmsg_retire_fakes()
        self.workdir = self.home_dir

        result = self.run_agmsg_retire_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Skipping agmsg retire for $HOME", result.stderr)
        self.assertEqual(result.stdout, "")
        calls = self.calls_path.read_text().splitlines() if self.calls_path.exists() else []
        self.assertFalse(any(call.startswith(("delivery ", "identities ", "leave ")) for call in calls), calls)

    def git_checkout(self, path: Path, origin: str | None, *, clone_of: Path | None = None) -> Path:
        """A checkout with one commit (or a clone of `clone_of`) and the given origin URL."""
        git = ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false"]
        if clone_of is not None:
            subprocess.run([*git, "clone", "-q", str(clone_of), str(path)], check=True, capture_output=True)
            subprocess.run([*git, "-C", str(path), "remote", "remove", "origin"], check=True, capture_output=True)
        else:
            path.mkdir(exist_ok=True)
            subprocess.run([*git, "init", "-q", str(path)], check=True, capture_output=True)
            subprocess.run(
                [*git, "-C", str(path), "commit", "-q", "--allow-empty", "-m", "init"], check=True, capture_output=True
            )
        if origin is not None:
            subprocess.run([*git, "-C", str(path), "remote", "add", "origin", origin], check=True, capture_output=True)
        return path.resolve()

    def write_registered_agmsg_store(self) -> dict[str, Path]:
        """A scratch team store registering five projects, with store-backed agmsg fakes.

        identities.sh reads the store as the real one does; leave.sh drops the member and
        removes a team left empty; delivery.sh strips the agmsg hooks of the project it names.
        """
        clone = self.git_checkout(self.workdir, "https://github.com/mryfmo/dotfiles.git")
        projects = {
            "clone": clone,
            # Same repository under another URL spelling: retired.
            "workspace": self.git_checkout(
                self.temp_dir / "workspace", "git@github.com:MryFmo/dotfiles", clone_of=clone
            ),
            "bare": self.git_checkout(self.temp_dir / "bare", "https://github.com/mryfmo/dotfiles/", clone_of=clone),
            # Same root, other owner: skipped.
            "fork": self.git_checkout(self.temp_dir / "fork", "https://github.com/someone/dotfiles", clone_of=clone),
            # Another repository (the reports-daily-ops case): skipped.
            "reports": self.git_checkout(self.temp_dir / "reports", None),
            "gone": self.temp_dir.resolve() / "gone",
        }
        scripts = self.home_dir / ".agents/skills/agmsg/scripts"
        scripts.mkdir(parents=True)
        teams = self.home_dir / ".agents/skills/agmsg/teams"
        roster = {
            "dotfiles-conformance": {
                "claude-deep-dot": "workspace",
                "claude-bare-dot": "bare",
                "claude-gone-dot": "gone",
            },
            # A team shared with another repository keeps its other member.
            "shared-ops": {"claude-shared-dot": "workspace", "claude-shared-reports": "reports"},
            "reports-daily-ops": {"claude-deep-reports": "reports"},
            "fork-team": {"claude-fork": "fork"},
        }
        for team, members in roster.items():
            self.write_agmsg_team(team, {name: [projects[key]] for name, key in members.items()})
        for key in ("workspace", "fork", "reports"):
            self.write_agmsg_session_hook(projects[key])
        for name, body in {
            "identities.sh": f"""printf 'identities %s\\n' "$*" >> {self.calls_path}
for c in {teams}/*/config.json; do
    jq -r --arg p "$1" --arg t "$2" '.name as $n | .agents | to_entries[] | select(any(.value.registrations[]; .project == $p and .type == $t)) | "\\($n)\\t\\(.key)"' "$c"
done
""",
            "leave.sh": f"""printf 'leave %s\\n' "$*" >> {self.calls_path}
c={teams}/$1/config.json
jq --arg n "$2" 'del(.agents[$n])' "$c" > "$c.new" && mv "$c.new" "$c"
[[ "$(jq '.agents | length' "$c")" != 0 ]] || rm -r {teams}/"$1"
""",
            "delivery.sh": f"""printf 'delivery %s\\n' "$*" >> {self.calls_path}
f="$4/.claude/settings.local.json"
jq 'del(.hooks)' "$f" > "$f.new" && mv "$f.new" "$f"
""",
        }.items():
            (scripts / name).write_text("#!/usr/bin/env bash\n" + body)
            (scripts / name).chmod(0o755)
        return projects

    def write_agmsg_team(self, team: str, members: dict[str, list[Path]]) -> Path:
        """A scratch team config whose members carry one claude-code registration per project."""
        config = self.home_dir / ".agents/skills/agmsg/teams" / team / "config.json"
        config.parent.mkdir(parents=True)
        agents = {
            name: {"registrations": [{"type": "claude-code", "project": str(p)} for p in paths]}
            for name, paths in members.items()
        }
        config.write_text(json.dumps({"name": team, "agents": agents}))
        return config

    def write_agmsg_session_hook(self, project: Path) -> Path:
        """A settings.local.json carrying one agmsg SessionStart hook for `project`."""
        scripts = self.home_dir / ".agents/skills/agmsg/scripts"
        settings = project / ".claude/settings.local.json"
        settings.parent.mkdir(exist_ok=True)
        command = f"'{scripts}/session-start.sh' 'claude-code' '{project}'"
        settings.write_text(
            json.dumps(
                {
                    "permissions": {"allow": ["Bash(git status:*)"]},
                    "hooks": {"SessionStart": [{"matcher": "", "hooks": [{"type": "command", "command": command}]}]},
                }
            )
        )
        return settings

    def run_registered_retire(self) -> subprocess.CompletedProcess[str]:
        """`herdr-agents --retire-agmsg` without DIR, from the clone, as `make agmsg-retire` runs it."""
        env = os.environ.copy()
        env["HOME"] = str(self.home_dir)
        env["PATH"] = f"{self.bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin"
        return subprocess.run(
            ["bash", str(SCRIPT), "--retire-agmsg"],
            cwd=self.workdir,
            env=env,
            check=False,
            text=True,
            capture_output=True,
        )

    def test_retire_agmsg_without_dir_retires_only_the_registered_clones_of_this_repository(self) -> None:
        p = self.write_registered_agmsg_store()
        teams = self.home_dir / ".agents/skills/agmsg/teams"
        untouched = {
            path: path.read_bytes()
            for path in (
                p["fork"] / ".claude/settings.local.json",
                p["reports"] / ".claude/settings.local.json",
                teams / "reports-daily-ops/config.json",
                teams / "fork-team/config.json",
            )
        }

        result = self.run_registered_retire()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = [c for c in self.calls_path.read_text().splitlines() if c.startswith(("delivery ", "leave "))]
        self.assertEqual(
            calls,
            [
                "leave dotfiles-conformance claude-bare-dot",
                f"delivery set off claude-code {p['workspace']}",
                "leave dotfiles-conformance claude-deep-dot",
                "leave shared-ops claude-shared-dot",
            ],
        )
        self.assertEqual(
            result.stdout,
            f"agmsg retire: registered project {p['bare']} (team dotfiles-conformance)\n"
            f"agmsg retire: no agmsg hook in {p['bare']}/.claude/settings.local.json (missing or none); hook removal skipped\n"
            "agmsg retired: claude-bare-dot left team dotfiles-conformance\n"
            f"agmsg retire: registered project {p['fork']} (team fork-team) is not a clone of this repository; skipped\n"
            f"agmsg retire: registered project {p['gone']} (team dotfiles-conformance) is gone; skipped\n"
            f"agmsg retire: registered project {p['reports']} (team reports-daily-ops,shared-ops) is not a clone of this repository; skipped\n"
            f"agmsg retire: registered project {p['workspace']} (team dotfiles-conformance,shared-ops)\n"
            f"agmsg retired: removed the agmsg hooks from {p['workspace']}/.claude/settings.local.json\n"
            "agmsg retired: claude-deep-dot left team dotfiles-conformance\n"
            "agmsg retired: claude-shared-dot left team shared-ops\n"
            f"agmsg already retired for {p['clone']}\n",
        )
        self.assertNotIn("hooks", json.loads((p["workspace"] / ".claude/settings.local.json").read_text()))
        for path, content in untouched.items():
            self.assertEqual(path.read_bytes(), content, path)
        self.assertEqual(
            set(json.loads((teams / "shared-ops/config.json").read_text())["agents"]), {"claude-shared-reports"}
        )

        self.calls_path.unlink()
        again = self.run_registered_retire()

        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertFalse(
            any(c.startswith(("delivery ", "leave ")) for c in self.calls_path.read_text().splitlines()),
            self.calls_path.read_text(),
        )
        self.assertTrue(again.stdout.endswith(f"agmsg already retired for {p['clone']}\n"), again.stdout)
        self.assertNotIn("agmsg retired:", again.stdout)

    def test_retire_agmsg_without_dir_fails_when_a_registered_clone_keeps_a_hook(self) -> None:
        p = self.write_registered_agmsg_store()
        (self.home_dir / ".agents/skills/agmsg/scripts/delivery.sh").write_text(
            f"#!/usr/bin/env bash\nprintf 'delivery %s\\n' \"$*\" >> {self.calls_path}\n"
        )

        result = self.run_registered_retire()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"agmsg hooks remain in {p['workspace']}/.claude/settings.local.json", result.stderr)
        self.assertNotIn("leave dotfiles-conformance claude-deep-dot", self.calls_path.read_text())

    def test_retire_agmsg_skips_an_identity_whose_team_is_gone(self) -> None:
        scripts = self.install_agmsg_retire_fakes()
        (self.workdir / ".claude/settings.local.json").write_text("{}")
        shutil.rmtree(self.home_dir / ".agents/skills/agmsg/teams/dotfiles-conformance")

        result = self.run_agmsg_retire_helper()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            result.stdout, "agmsg retire: team dotfiles-conformance of claude-orchestrator no longer exists; skipped\n"
        )
        self.assertFalse(any(c.startswith("leave ") for c in self.calls_path.read_text().splitlines()))
        self.assertTrue((scripts / "leave.sh").exists())

    def test_retire_agmsg_without_dir_keeps_a_membership_also_registered_outside_this_repository(self) -> None:
        p = self.write_registered_agmsg_store()
        # join.sh appends a registration per project to one member; leave.sh would drop all of them.
        mixed = self.write_agmsg_team("mixed-ops", {"claude-mixed": [p["workspace"], p["reports"]]})
        # A member registered only at clones of this repository still leaves.
        clones = self.write_agmsg_team("clone-ops", {"claude-two-clones": [p["bare"], p["workspace"]]})
        before = mixed.read_bytes()

        result = self.run_registered_retire()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            f"agmsg retire: claude-mixed in team mixed-ops is also registered at {p['reports']}; membership kept\n",
            result.stdout,
        )
        calls = self.calls_path.read_text().splitlines()
        self.assertNotIn("leave mixed-ops claude-mixed", calls)
        self.assertEqual(mixed.read_bytes(), before)
        # The clone's hooks still go, and its single-repository members still leave.
        self.assertIn(f"delivery set off claude-code {p['workspace']}", calls)
        self.assertNotIn("hooks", json.loads((p["workspace"] / ".claude/settings.local.json").read_text()))
        self.assertEqual([c for c in calls if c.startswith("leave clone-ops")], ["leave clone-ops claude-two-clones"])
        self.assertFalse(clones.exists())
        self.assertIn("leave dotfiles-conformance claude-deep-dot", calls)

    def test_retire_agmsg_without_dir_carries_a_tab_in_a_registered_path(self) -> None:
        p = self.write_registered_agmsg_store()
        # The registered clone's path is its unregistered neighbour's path plus a tab and a suffix.
        prefix = self.git_checkout(self.temp_dir / "tabbed", "https://github.com/mryfmo/dotfiles", clone_of=p["clone"])
        tabbed = self.git_checkout(
            self.temp_dir / "tabbed\tsuffix", "https://github.com/mryfmo/dotfiles", clone_of=p["clone"]
        )
        self.write_agmsg_team("tab-ops", {"claude-tab": [tabbed]})
        self.write_agmsg_session_hook(tabbed)
        prefix_settings = self.write_agmsg_session_hook(prefix)
        before = prefix_settings.read_bytes()

        result = self.run_registered_retire()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"agmsg retire: registered project {tabbed} (team tab-ops)\n", result.stdout)
        calls = self.calls_path.read_text().splitlines()
        self.assertIn(f"delivery set off claude-code {tabbed}", calls)
        self.assertIn("leave tab-ops claude-tab", calls)
        self.assertNotIn("hooks", json.loads((tabbed / ".claude/settings.local.json").read_text()))
        self.assertFalse(any(c == f"delivery set off claude-code {prefix}" for c in calls), calls)
        self.assertNotIn(f"registered project {prefix} ", result.stdout)
        self.assertEqual(prefix_settings.read_bytes(), before)

    def test_retire_agmsg_without_dir_keeps_a_member_with_another_type_registered_outside_this_repository(
        self,
    ) -> None:
        p = self.write_registered_agmsg_store()
        # leave.sh drops the whole member whatever the type, so a codex registration counts too.
        mixed = self.write_agmsg_team("mixed-type-ops", {"claude-mixed-type": [p["workspace"]]})
        config = json.loads(mixed.read_text())
        config["agents"]["claude-mixed-type"]["registrations"].append({"type": "codex", "project": str(p["reports"])})
        mixed.write_text(json.dumps(config))
        before = mixed.read_bytes()

        result = self.run_registered_retire()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            f"agmsg retire: claude-mixed-type in team mixed-type-ops is also registered at {p['reports']};"
            " membership kept\n",
            result.stdout,
        )
        calls = self.calls_path.read_text().splitlines()
        self.assertNotIn("leave mixed-type-ops claude-mixed-type", calls)
        self.assertEqual(mixed.read_bytes(), before)
        self.assertIn(f"delivery set off claude-code {p['workspace']}", calls)
        self.assertNotIn("hooks", json.loads((p["workspace"] / ".claude/settings.local.json").read_text()))

    def test_retire_agmsg_without_dir_exits_1_on_an_unreadable_team_config(self) -> None:
        self.write_registered_agmsg_store()
        broken = self.home_dir / ".agents/skills/agmsg/teams/dotfiles-conformance/config.json"
        broken.write_text('{"agents": {')

        result = self.run_registered_retire()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"cannot read {broken} as JSON", result.stderr)
        calls = self.calls_path.read_text().splitlines() if self.calls_path.exists() else []
        self.assertFalse(any(c.startswith(("leave ", "delivery ")) for c in calls), calls)

    def test_retire_agmsg_without_dir_leaves_nothing_when_the_membership_read_fails(self) -> None:
        self.write_registered_agmsg_store()
        # Fail only the membership guard's read (`.agents[$n] //`, in this and the earlier guard), after the
        # store listing and identities.sh succeeded; the fake leave.sh's `del(.agents[$n])` is not matched.
        jq = self.bin_dir / "jq"
        real = os.path.realpath(jq)
        jq.unlink()
        self.write_executable(
            "jq",
            f"""#!/usr/bin/env bash
for arg in "$@"; do
    [[ $arg != *'.agents[$n] //'* ]] || {{ printf 'jq: injected read failure\\n' >&2; exit 2; }}
done
exec {real} "$@"
""",
        )
        config = self.home_dir / ".agents/skills/agmsg/teams/dotfiles-conformance/config.json"

        result = self.run_registered_retire()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"cannot read the registrations of claude-bare-dot in {config}", result.stderr)
        calls = self.calls_path.read_text().splitlines()
        self.assertFalse(any(c.startswith("leave ") for c in calls), calls)
        self.assertNotIn("left team", result.stdout)

    RETIRED_STUB = (
        "#!/usr/bin/env bash\n"
        "# herdr-agents main-push guard: written by herdr-agents --bootstrap-agmsg; the checks live in herdr-agents --main-push-guard.\n"
        'guard="$(command -v herdr-agents)" || guard="${HOME}/.local/bin/common/herdr-agents"\n'
        'if [[ -x ${guard} && "$("${guard}" --help 2> /dev/null)" == *--main-push-guard* ]]; then\n'
        '    exec "${guard}" --main-push-guard "$@"\n'
        "fi\n"
        "# No launcher with the guard mode (missing, or older than the guard): refuse main updates only.\n"
        "status=0\n"
        "while read -r _ _ remote_ref _; do\n"
        "    if [[ ${remote_ref} == refs/heads/main ]]; then\n"
        "        printf 'pre-push: no herdr-agents with --main-push-guard is installed (run make update), so this push to main is refused\\n' >&2\n"
        "        status=1\n"
        "    fi\n"
        "done\n"
        'exit "${status}"\n'
    )

    def init_git_workdir(self, hooks_path: str | None = None) -> Path:
        """Make the retire workdir a git main checkout; returns its pre-push hook path."""
        result = subprocess.run(
            ["git", "init", "-q", "-b", "main", str(self.workdir)], check=False, text=True, capture_output=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        hooks = self.workdir / ".git/hooks"
        if hooks_path is not None:
            config = ["git", "-C", str(self.workdir), "config", "core.hooksPath", hooks_path]
            self.assertEqual(subprocess.run(config, check=False).returncode, 0)
            hooks = self.workdir / hooks_path
        hooks.mkdir(parents=True, exist_ok=True)
        return hooks / "pre-push"

    def test_retire_removes_the_retired_pre_push_stub(self) -> None:
        self.install_agmsg_fakes()
        for hooks_path in (None, ".git/custom-hooks"):
            with self.subTest(hooks_path=hooks_path):
                shutil.rmtree(self.workdir / ".git", ignore_errors=True)
                hook = self.init_git_workdir(hooks_path)
                hook.write_text(self.RETIRED_STUB)
                hook.chmod(0o755)
                log = self.workdir / ".git/orch-push-main.log"
                log.write_text("2026-10-02T00:00:00Z refused refs/heads/main:refs/heads/main\n")

                result = self.run_agmsg_retire_helper()

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse(hook.exists())
                self.assertFalse(log.exists())
                self.assertIn(f"removed the retired main-push guard stub at {hook.resolve()}", result.stderr)

    def test_retire_leaves_a_foreign_pre_push_hook_alone(self) -> None:
        self.install_agmsg_fakes()
        edited = self.RETIRED_STUB.replace('exit "${status}"\n', './scripts/local-checks.sh\nexit "${status}"\n')
        self.assertNotEqual(edited, self.RETIRED_STUB)
        for name, content, notice, hooks_path in (
            ("foreign", "#!/bin/sh\nexit 0\n", False, None),
            ("edited stub", edited, True, None),
            ("exact stub outside the common git dir", self.RETIRED_STUB, False, "shared-hooks"),
            # Under `* text` the clean filter normalizes CRLF, so only a raw-byte
            # hash (--no-filters) tells this copy from the stub.
            ("CRLF stub under a text .gitattributes", self.RETIRED_STUB.replace("\n", "\r\n"), True, None),
        ):
            with self.subTest(hook=name):
                shutil.rmtree(self.workdir / ".git", ignore_errors=True)
                if "gitattributes" in name:
                    (self.workdir / ".gitattributes").write_text("* text\n")
                hook = self.init_git_workdir(hooks_path)
                hook.write_bytes(content.encode())
                log = self.workdir / ".git/orch-push-main.log"
                log.write_text("kept\n")

                result = self.run_agmsg_retire_helper()

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(hook.read_bytes(), content.encode())
                self.assertEqual(log.read_text(), "kept\n")
                self.assertNotIn("removed the retired main-push guard stub", result.stderr)
                self.assertEqual(
                    f"{hook.resolve()} is an edited copy of the retired main-push guard stub" in result.stderr, notice
                )

    @unittest.skipIf(os.geteuid() == 0, "root reads a mode-000 file")
    def test_retire_refuses_when_the_pre_push_hook_cannot_be_read(self) -> None:
        self.install_agmsg_fakes()
        hook = self.init_git_workdir()
        hook.write_text(self.RETIRED_STUB)
        hook.chmod(0o000)

        result = self.run_agmsg_retire_helper()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"cannot hash {hook.resolve()}", result.stderr)
        self.assertNotIn("removed the retired main-push guard stub", result.stderr)
        hook.chmod(0o644)
        self.assertEqual(hook.read_text(), self.RETIRED_STUB)

    def test_make_update_retires_agmsg_and_upgrade_is_gone(self) -> None:
        result = subprocess.run(
            ["make", "-n", "-f", str(MAKEFILE), "update"],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("make agmsg-retire", result.stdout)
        self.assertNotIn("agmsg-bootstrap", result.stdout)
        # The retire runs the installed agmsg tree's scripts, so it comes before the apply that removes it (U26).
        self.assertLess(result.stdout.index("make agmsg-retire"), result.stdout.index("chezmoi apply --verbose"))

        upgrade = subprocess.run(
            ["make", "-n", "-f", str(MAKEFILE), "upgrade"],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertNotEqual(upgrade.returncode, 0, upgrade.stdout)
        self.assertIn("No rule to make target", upgrade.stderr)

    def test_the_installed_attach_session_hook_leaves_and_other_hooks_stay(self) -> None:
        # U26: --attach claimed an agmsg seat and left with it, so the merge drops an installed hook that runs it.
        source_dir = self.temp_dir / "source"
        (source_dir / ".chezmoitemplates").mkdir(parents=True)
        state_hook = {"type": "command", "command": f"{self.home_dir}/.claude/hooks/herdr-agent-state.sh start"}
        (source_dir / ".chezmoitemplates/claude-settings-managed.json").write_text(
            json.dumps({"hooks": {"SessionStart": [{"matcher": "*", "hooks": [state_hook]}]}}) + "\n"
        )
        attach = f'{self.home_dir}/.local/bin/common/herdr-agents --attach 2>> "$HOME/.config/herdr/herdr-agents.log" || true'
        operator_hook = {"type": "command", "command": "echo operator"}
        installed = {
            "hooks": {
                "SessionStart": [
                    {"matcher": "*", "hooks": [state_hook]},
                    {"matcher": "*", "hooks": [{"type": "command", "command": attach, "timeout": 10}]},
                    {"matcher": "startup", "hooks": [operator_hook]},
                ]
            }
        }
        env = os.environ | {"CHEZMOI_SOURCE_DIR": str(source_dir), "CHEZMOI_HOME_DIR": str(self.home_dir)}

        def merge(current: str) -> str:
            result = subprocess.run(
                [sys.executable, str(CLAUDE_SETTINGS_MODIFIER)],
                input=current,
                env=env,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return result.stdout

        merged = merge(json.dumps(installed))
        session_start = json.loads(merged)["hooks"]["SessionStart"]
        self.assertNotIn("herdr-agents --attach", merged)
        self.assertEqual(
            session_start,
            [{"matcher": "*", "hooks": [state_hook]}, {"matcher": "startup", "hooks": [operator_hook]}],
        )
        self.assertEqual(merge(merged), merged, "a second merge is byte-identical")
        fresh = json.loads(merge(""))["hooks"]["SessionStart"]
        self.assertEqual(fresh, [{"matcher": "*", "hooks": [state_hook]}], "a fresh install has no attach hook")

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
            [
                "bash",
                "-c",
                config["opener"]["edit"][0]["run"].replace("%s", "example.txt"),
            ],
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
            [
                "bash",
                "-c",
                config["opener"]["edit"][0]["run"].replace("%s", "example.txt"),
            ],
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(zed_calls.read_text(), "--add example.txt\n")
        self.assertFalse(editor_calls.exists())

    def test_ghostty_config_does_not_auto_start_herdr_session(self) -> None:
        self.assertNotIn("initial-command", GHOSTTY_CONFIG.read_text())

    def test_zprofile_adds_common_bin_to_login_shell_path(self) -> None:
        zprofile = ZPROFILE.read_text()
        zshrc = ZSHRC.read_text()

        self.assertIn("typeset -gU path", zprofile)
        self.assertIn('"${HOME}/.local/bin/common"', zprofile)
        self.assertIn('if [[ -d "${directory}" ]]', zprofile)
        self.assertNotIn("typeset -gU path fpath", zshrc)


if __name__ == "__main__":
    unittest.main()
