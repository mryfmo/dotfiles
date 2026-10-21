"""Inspect administrative policy and nonprivileged staging in temporary homes."""

import json
import os
import subprocess
import unittest

from tests.unit.test_claude_worker_settings import expand
from tests.unit.test_generate_agent_configs import ROOT


class ClaudeManagedSettingsTest(unittest.TestCase):
    def setUp(self):
        from tests.unit.test_claude_worker_settings import ClaudeWorkerSettingsTest

        ClaudeWorkerSettingsTest.setUp(self)

    def test_rendered_policy_requires_admin_sandbox(self):
        for platform in ("darwin", "linux"):
            policy = expand(self.module.render_claude_managed_settings(self.manifest), self.home, platform)["sandbox"]
            for key in ("enabled", "failIfUnavailable"):
                self.assertIs(policy[key], True)
            for key in "allowUnsandboxedCommands enableWeakerNestedSandbox enableWeakerNetworkIsolation allowAppleEvents".split():
                self.assertIs(policy[key], False)
            self.assertEqual(policy["filesystem"], {"disabled": False})
            self.assertEqual(
                policy["network"],
                {
                    "allowAllUnixSockets": False,
                    "allowLocalBinding": False,
                    "allowUnixSockets": [str(self.home / ".config/herdr/herdr.sock")],
                },
            )
            self.assertEqual(
                policy["excludedCommands"],
                [
                    "agmsg-dispatch *",
                    "herdr-agents *",
                    str(self.home / ".agents/skills/agmsg/scripts/actas-claim.sh") + " *",
                ],
            )

    def test_managed_render_is_independent_of_conflicting_project_and_local_settings(self):
        before = self.module.render_claude_managed_settings(self.manifest)
        for name in ("settings.json", "settings.local.json"):
            target = self.home / "project/.claude" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(
                    {
                        "sandbox": {
                            "enabled": False,
                            "failIfUnavailable": False,
                            "excludedCommands": ["*"],
                            "allowUnsandboxedCommands": True,
                            "enableWeakerNestedSandbox": True,
                            "enableWeakerNetworkIsolation": True,
                            "filesystem": {"disabled": True, "allowWrite": ["/"]},
                            "network": {"allowAllUnixSockets": True, "allowUnixSockets": ["/tmp/poison.sock"]},
                        }
                    }
                )
            )
        self.assertEqual(before, self.module.render_claude_managed_settings(self.manifest))

    def test_install_target_stages_and_prints_without_running_sudo(self):
        fakebin = self.home / "bin"
        fakebin.mkdir()
        sudo = fakebin / "sudo"
        sudo.write_text("#!/bin/sh\ntouch '" + str(self.home / "sudo-ran") + "'\n")
        sudo.chmod(0o755)
        uname = fakebin / "uname"
        for platform, admin in (
            ("Darwin", "/Library/Application Support/ClaudeCode/managed-settings.json"),
            ("Linux", "/etc/claude-code/managed-settings.json"),
        ):
            uname.write_text("#!/bin/sh\nprintf '%s\\n' " + platform + "\n")
            uname.chmod(0o755)
            result = subprocess.run(
                ["make", "--no-print-directory", "install-managed-settings"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                env=dict(os.environ, HOME=str(self.home), PATH=str(fakebin) + ":" + os.environ["PATH"]),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            staging = self.home / ".claude/managed-settings.rendered.json"
            expected = expand(self.module.render_claude_managed_settings(self.manifest), self.home, platform.lower())
            self.assertEqual(json.loads(staging.read_text()), expected)
            self.assertEqual(result.stdout.strip(), f'sudo install -m 0644 "{staging}" "{admin}"')
            self.assertFalse((self.home / "sudo-ran").exists())


if __name__ == "__main__":
    unittest.main()
