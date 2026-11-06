"""Which of the kit's Claude hooks the dsh-hooks-claude-code bridge runs (regime-cutover U179, U298).

The thak profile mounts `@deepseek-ai/dsh-hooks-claude-code` over the deployed `~/.claude/settings.json`. Two closed
facts decide what runs. First, activation: cordis calls the plugin's `apply()` only once every service it injects has an
enabled provider, and the kit's patch disables the base bundle's `bash-sandbox` row, the one `shell` provider on this
platform, so the plugin stays `pending (waiting for service: shell)` and registers no listener (measured 2026-11-06 on
the deployed laptop, U298: the d22 turn answered pong, no `.epoch` file appeared, DSH printed that warning). Second, the
matcher rule: the bridge runs seven Claude Code events and compares tool matchers as exact strings against DSH's
model-visible tool names. Both are held here as constants measured upstream at the pinned tag (the plugin's injected
services and their provider rows, the event tuple, the literal-matcher rule, the tool catalog's names) and the table is
computed from them against the settings template and the kit's patch, so it fails by name when a hook group is added, a
matcher's coverage changes, the pin moves, the mount stops naming the deployed settings, or the patch enables or disables
a provider of an injected service. Nothing here runs a hook or reads the network.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
import unittest
from itertools import zip_longest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETTINGS_TEMPLATE = ROOT / "home/.chezmoitemplates/claude-settings-managed.json"
SETTINGS_MODIFIER = ROOT / "home/dot_claude/modify_private_settings.json"
PATCH = ROOT / "home/dot_dsh/profiles/thak/cordis.patch.yml"

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from test_generate_agent_configs import load_manifest_fixture
from test_dsh_profile import rows

# The tag the constants below were measured at (manifest assets.deepseek-harness.pin).
MEASURED_PIN = "dsh-v0.2.1-rc.5"
# packages/experimental/hooks-claude-code/src/config.ts CLAUDE_EVENTS at dsh-v0.2.1-rc.5; other events are ignored.
BRIDGE_EVENTS = frozenset(
    {"SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop", "SubagentStart", "SubagentStop"}
)
# packages/experimental/hooks-claude-code/src/index.ts at dsh-v0.2.1-rc.5: what the matcher is tested against per event
# (None: the matcher is discarded).
MATCHER_SUBJECT = {
    "PreToolUse": "tool",
    "PostToolUse": "tool",
    "SessionStart": "source",
    "SubagentStart": "agent_type",
    "SubagentStop": "agent_type",
    "UserPromptSubmit": None,
    "Stop": None,
}
# docs/tool-catalog.md "Tool Package Map" at dsh-v0.2.1-rc.5: the model-visible tool names a PreToolUse or PostToolUse
# matcher is compared with.
DSH_TOOL_NAMES = frozenset(
    {
        "plugin_manager",
        "plugin_market",
        "list_mcp_resource_templates",
        "list_mcp_resources",
        "read_mcp_resource",
        "stagehand_act",
        "stagehand_extract",
        "stagehand_navigate",
        "stagehand_observe",
        "stagehand_screenshot",
        "stagehand_tabs",
        "ask_user_question",
        "run_code",
        "exit_plan_mode",
        "bash",
        "present",
        "pwsh",
        "cordis_inspect_list",
        "cordis_inspect_query",
        "str_replace_editor",
        "edit",
        "read",
        "read_image",
        "write",
        "glob",
        "grep",
        "terminal_close",
        "terminal_list",
        "terminal_open",
        "terminal_read",
        "terminal_send",
        "terminal_signal",
        "create_goal",
        "get_goal",
        "update_goal",
        "schedule_create",
        "schedule_delete",
        "schedule_list",
        "schedule_update",
        "lsp",
        "ralph",
        "skill",
        "session_event_read",
        "session_event_search",
        "session_event_trace",
        "session_search",
        "session_trace",
        "list_subagent_models",
        "subagent",
        "subagent_fork",
        "interrupt_agent",
        "list_agents",
        "send_message",
        "job_kill",
        "job_list",
        "job_output",
        "spawn_teammate",
        "team_task_create",
        "team_task_get",
        "team_task_list",
        "team_task_update",
        "wait_agent",
        "todo_write",
        "working_directory",
        "create_worktree",
        "workflow",
        "load_workspace_dependencies",
        "web_fetch",
        "web_search",
    }
)
# packages/experimental/hook-protocol/src/matcher.ts at dsh-v0.2.1-rc.5: this form is split on `|` and compared as
# exact strings; any other matcher is compiled as a regular expression.
LITERAL_MATCHER = re.compile(r"^[A-Za-z0-9_]+(\|[A-Za-z0-9_]+)*$")
# packages/experimental/hooks-claude-code/src/index.ts `inject` at dsh-v0.2.1-rc.5: cordis calls the plugin's apply()
# only once each of these services has an enabled provider; until then the plugin is `pending (waiting for service:
# <name>)`, the startup warning names it and no listener (agent/created, tools/pre-execute, ...) is registered.
BRIDGE_INJECTED_SERVICES = frozenset({"shell", "sessionProjections", "workingDirectory"})
# packages/bundle/base/cordis.patch.yml at dsh-v0.2.1-rc.5: the base bundle rows that register each injected service on
# a non-Windows host. `shell` is ShellExecutor (packages/shell/shell/src/index.ts, `super(ctx, 'shell')`), registered
# by bash-sandbox's SandboxBashExecutor alone (pwsh-sandbox is disabled unless win32); sessionProjections and
# workingDirectory are the session-projection and working-directory rows. A service missing here fails by name.
SERVICE_PROVIDER_ROWS = {
    "shell": frozenset({"bash-sandbox"}),
    "sessionProjections": frozenset({"session-projection"}),
    "workingDirectory": frozenset({"working-directory"}),
}
# The coverage measured at dsh-v0.2.1-rc.5 for the kit's hook groups, in the settings template's order: what runs under
# the kit's profile as deployed, then what the matcher rule would run once the plugin activates. `inactive` on every row
# is the 2026-11-06T16:36Z measurement (U298): `DSH_HOME=$HOME/.dsh ~/.dsh/bin/dsh --profile thak 'Reply with the single
# word pong.'` answered pong with status 0, ~/.local/state/agent-staleness held 18 .epoch files before and after, and
# stderr carried `hooks-claude-code (@deepseek-ai/dsh-hooks-claude-code): pending (waiting for service: shell)`.
EXPECTED_COVERAGE = (
    ("PreToolUse", "Bash", "inactive", "uncovered"),
    ("SessionStart", "^(startup|resume|clear|compact|fork)$", "inactive", "unverified"),
    ("SessionStart", "*", "inactive", "covered"),
    ("PostToolUse", "Write|Edit", "inactive", "uncovered"),
    ("PermissionRequest", "*", "inactive", "uncovered"),
)
# The manifest's claude.hooks keys that name a hook script (home/dot_agents/agent-config.yaml).
MANIFEST_SCRIPT_KEYS = ("enforce_uv_hook", "format_edited_files_hook", "project_map_reload_hook")
HOME_DIR_TEMPLATE = "{{ .chezmoi.homeDir }}"
# The template's one conditional block, the `sandbox` value; home/dot_claude/modify_private_settings.json renders it
# by host, this loader keeps the first branch because the `hooks` key lies outside it and reads the same either way.
OS_BLOCK = re.compile(r'\{\{ if eq \.chezmoi\.os "darwin" \}\}(.*?)\{\{ else \}\}.*?\{\{ end \}\}', re.DOTALL)


def kit_hooks() -> dict[str, list[dict]]:
    """The `hooks` mapping of the settings template, with the home directory rendered as `~`."""
    text = OS_BLOCK.sub(lambda match: match[1], SETTINGS_TEMPLATE.read_text()).replace(HOME_DIR_TEMPLATE, "~")
    return json.loads(text)["hooks"]


def disabled_rows(patch: str) -> frozenset[str]:
    """The ids of the top-level rows the kit's patch marks `disabled: true`."""
    return frozenset(
        key.removeprefix("id: ")
        for key, block in rows(patch).items()
        if key.startswith("id: ") and re.search(r"^  disabled: true$", block, re.MULTILINE)
    )


def missing_services(patch: str) -> frozenset[str]:
    """The services the bridge injects whose every provider row the kit's patch disables; non-empty means `inactive`."""
    disabled = disabled_rows(patch)
    return frozenset(service for service in BRIDGE_INJECTED_SERVICES if SERVICE_PROVIDER_ROWS[service] <= disabled)


def matcher_coverage(event: str, matcher: str | None) -> str:
    """Whether the bridge at MEASURED_PIN, once active, would run a hook group: `covered`, `uncovered` or `unverified`."""
    if event not in BRIDGE_EVENTS:
        return "uncovered"
    if matcher in (None, "", "*") or MATCHER_SUBJECT[event] is None:
        return "covered"
    if MATCHER_SUBJECT[event] == "tool":
        if not LITERAL_MATCHER.match(matcher):
            return "unverified"
        return "covered" if set(matcher.split("|")) & DSH_TOOL_NAMES else "uncovered"
    return "unverified"


def coverage(event: str, matcher: str | None, missing: frozenset[str]) -> str:
    """What runs under the kit's profile: `inactive` while an injected service lacks a provider, else the matcher verdict."""
    return "inactive" if missing else matcher_coverage(event, matcher)


def first_command(group: dict) -> str:
    return group["hooks"][0]["command"] if group.get("hooks") else "(no command)"


def describe(event: str, matcher: str | None, command: str) -> str:
    return f"{event} matcher {matcher!r} ({command})"


class DshHookCoverageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = Path(tempfile.mkdtemp(prefix="dsh-hook-coverage-test-"))
        cls.manifest = load_manifest_fixture(cls.temp_dir)
        cls.hooks = kit_hooks()
        cls.groups = [(event, group) for event, groups in cls.hooks.items() for group in groups]
        cls.patch = PATCH.read_text()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp_dir)

    def test_the_table_is_measured_at_the_manifest_pin(self) -> None:
        pin = self.manifest["assets"]["deepseek-harness"]["pin"]
        self.assertEqual(
            MEASURED_PIN,
            pin,
            f"the manifest pins deepseek-harness at {pin} but the coverage table was measured at {MEASURED_PIN}: "
            "re-measure config.ts, matcher.ts and docs/tool-catalog.md at the new tag and update the constants",
        )

    def test_every_kit_hook_group_has_the_coverage_the_table_says(self) -> None:
        missing = missing_services(self.patch)
        computed = [
            (event, matcher, coverage(event, matcher, missing), matcher_coverage(event, matcher))
            for event, matcher in ((event, group.get("matcher")) for event, group in self.groups)
        ]
        for index, (got, want) in enumerate(zip_longest(computed, EXPECTED_COVERAGE)):
            if got == want:
                continue
            command = first_command(self.groups[index][1]) if index < len(self.groups) else "(no group)"
            got_text = (
                f"{describe(got[0], got[1], command)}: computed {got[2]} (once active {got[3]})" if got else "no group"
            )
            want_text = (
                f"{describe(want[0], want[1], 'expected')}: expected {want[2]} (once active {want[3]})"
                if want
                else "no row"
            )
            self.fail(f"hook group {index} differs from the coverage table: {got_text}; {want_text}")

    def test_the_hooks_plugin_waits_for_the_shell_service_the_kit_profile_disables(self) -> None:
        # Measured 2026-11-06T16:36Z on the deployed laptop (U298 finding): the d22 turn answered pong, status 0, the
        # .epoch count stayed 18, and DSH warned `3 entries did not activate ... hooks-claude-code
        # (@deepseek-ai/dsh-hooks-claude-code): pending (waiting for service: shell)`; the bash-sandbox row is off by
        # design (agent-config.yaml, deepseek-harness reason: the seat boundary is srt or nothing). A patch that enables
        # it or inserts another ShellExecutor activates the plugin and the table's third column must change with it.
        self.assertEqual(
            frozenset({"shell"}),
            missing_services(self.patch),
            f"{PATCH.name} disables {sorted(disabled_rows(self.patch))}; the bridge injects "
            f"{sorted(BRIDGE_INJECTED_SERVICES)} and the table's `inactive` column rests on `shell` alone being unprovided",
        )
        self.assertIn("- id: bash-sandbox\n  disabled: true\n", self.patch)
        for service in BRIDGE_INJECTED_SERVICES:
            self.assertTrue(
                SERVICE_PROVIDER_ROWS.get(service),
                f"injected service {service} names no provider row: re-measure packages/bundle/base/cordis.patch.yml",
            )
        self.assertEqual(
            {"inactive"},
            {runs for _event, _matcher, runs, _once_active in EXPECTED_COVERAGE},
            "a missing service makes every row inactive; the table's third column disagrees",
        )

    def test_the_three_manifest_hook_scripts_sit_in_groups_the_table_knows(self) -> None:
        known = {(event, matcher) for event, matcher, _runs, _once_active in EXPECTED_COVERAGE}
        for key in MANIFEST_SCRIPT_KEYS:
            script = self.manifest["claude"]["hooks"][key]
            holders = [
                (event, group)
                for event, group in self.groups
                if any(script in hook["command"] for hook in group["hooks"])
            ]
            self.assertEqual(
                1,
                len(holders),
                f"{key} ({script}) is named by {len(holders)} hook groups: "
                + ", ".join(describe(event, group.get("matcher"), first_command(group)) for event, group in holders),
            )
            event, group = holders[0]
            self.assertIn(
                (event, group.get("matcher")),
                known,
                f"{describe(event, group.get('matcher'), first_command(group))} holds {key} "
                "but has no row in EXPECTED_COVERAGE: measure it and add the row",
            )

    def test_the_mount_reads_the_settings_file_the_kit_deploys(self) -> None:
        self.assertIn("name: '@deepseek-ai/dsh-hooks-claude-code'", self.patch, PATCH.name)
        config_path = re.search(r"^\s*configPath: (.*)$", self.patch, re.MULTILINE)
        self.assertIsNotNone(config_path, f"{PATCH.name} mounts the bridge without a configPath")
        literal = re.search(r"'([^']*)'", config_path[1])
        self.assertIsNotNone(literal, f"configPath {config_path[1]} has no single-quoted literal")
        self.assertTrue(
            literal[1].endswith("/.claude/settings.json"),
            f"the mount's configPath {config_path[1]} does not name ~/.claude/settings.json, the file the kit's "
            f"hook groups ({', '.join(sorted(self.hooks))}) are deployed into",
        )
        # The file at that path is the rendered settings template: the chezmoi modifier of ~/.claude/settings.json
        # reads the same template kit_hooks() reads.
        self.assertIn(
            SETTINGS_TEMPLATE.name,
            SETTINGS_MODIFIER.read_text(),
            f"{SETTINGS_MODIFIER.name} no longer renders {SETTINGS_TEMPLATE.name} into ~/.claude/settings.json",
        )

    def test_the_bridge_tool_names_are_lower_case_and_the_kit_matchers_are_not(self) -> None:
        self.assertEqual(sorted(DSH_TOOL_NAMES), sorted(name.lower() for name in DSH_TOOL_NAMES))
        for event, group in self.groups:
            matcher = group.get("matcher")
            if MATCHER_SUBJECT.get(event) != "tool" or not matcher or not LITERAL_MATCHER.match(matcher):
                continue
            # The fact behind the two uncovered tool rows: Claude Code names tools `Bash`, `Write`, `Edit`; DSH names
            # them `bash`, `write`, `edit`; the bridge compares the strings exactly.
            for literal in matcher.split("|"):
                self.assertFalse(
                    literal in DSH_TOOL_NAMES,
                    f"{describe(event, matcher, first_command(group))}: {literal} is a DSH tool name, so the "
                    "coverage table's row for this group must change",
                )


if __name__ == "__main__":
    unittest.main()
