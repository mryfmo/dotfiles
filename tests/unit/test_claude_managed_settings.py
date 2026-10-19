"""Inspect administrative policy and nonprivileged staging in temporary homes."""

import json
import os
from pathlib import Path
import shlex
import subprocess
import unittest

from tests.unit.test_claude_worker_settings import expand
from tests.unit.test_generate_agent_configs import ROOT, all_hooks, install_binding_fixture, render_claude_template


def prepare_bound_hooks(test):
    tools = install_binding_fixture(test.home)
    execution = test.manifest["claude"]["execution"]
    execution["tool_paths"] = dict.fromkeys(execution["tool_paths"], "/usr/bin/true") | tools
    anchor = test.home / "anchor"
    anchor.mkdir(exist_ok=True)
    test.manifest["claude"]["orchestrator_checkout"] = str(anchor)
    text = test.module.render_orchestrator_guard(
        test.manifest, (ROOT / "home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl").read_text()
    )
    guard = test.home / ".claude/hooks/orchestrator-only.sh"
    guard.parent.mkdir(parents=True, exist_ok=True)
    guard.write_text(render_claude_template(text, test.home, home=str(test.home), raw=True))
    guard.chmod(0o755)
    policy = json.loads(
        shlex.split(next(line[7:] for line in guard.read_text().splitlines() if line.startswith("policy=")))[0]
    )
    for entry in policy["commands"].values():
        argv = entry["argv"]
        path = Path(argv[2] if argv[1] == "-I" else argv[1])
        path = Path(str(path).replace("{checkout}", str(anchor)))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "from pathlib import Path\nPath(" + repr(str(test.home / "hook-ran")) + ").touch()\n"
            if argv[1] == "-I"
            else "#!/bin/bash\n/usr/bin/touch " + shlex.quote(str(test.home / "hook-ran")) + "\n"
        )
        path.chmod(0o755)
    for name in ("session-start", "session-end", "check-inbox"):
        path = test.home / ".agents/skills/agmsg/scripts" / (name + ".sh")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/bash\n/usr/bin/true\n")
        path.chmod(0o755)
    permgate = test.home / ".local/bin/common/permgate"
    permgate.parent.mkdir(parents=True, exist_ok=True)
    permgate.write_bytes((ROOT / "home/dot_local/bin/common/executable_permgate").read_bytes())
    permgate.chmod(0o755)
    protected = test.home / ".agents/permgate-policy.yaml"
    protected.parent.mkdir(parents=True, exist_ok=True)
    protected.write_text(
        json.dumps(
            {"schema_version": 3, "allow_patterns": [{"tool": "Bash", "regex": "^git status$"}], "deny_patterns": []}
        )
    )
    settings = render_claude_template(test.module.render_claude_settings(test.manifest), test.home, home=str(test.home))
    command = settings["hooks"]["PermissionRequest"][0]["hooks"][0]["command"]
    payload = json.dumps(
        {"hook_event_name": "PermissionRequest", "tool_name": "Bash", "tool_input": {"command": "git status"}}
    )
    return tools, anchor, guard, policy, settings, command, payload


class ClaudeManagedSettingsTest(unittest.TestCase):
    def setUp(self):
        from tests.unit.test_claude_worker_settings import ClaudeWorkerSettingsTest

        ClaudeWorkerSettingsTest.setUp(self)

    def test_rendered_hooks_bind_executables_and_permgate_returns_decision(self):
        tools, anchor, guard, policy, settings, command, payload = prepare_bound_hooks(self)
        self.assertIn(" run --no-config --no-project --offline --python ", command)
        self.assertIn(" python -I ", command)
        env = {
            "HOME": str(self.home),
            "PATH": "/usr/bin:/bin",
            "CLAUDE_PROJECT_DIR": str(anchor),
            "CLAUDE_ENV_FILE": str(self.home / "env"),
        }
        user_site = Path(
            subprocess.check_output(
                [tools["python3"], "-I", "-c", "import site; print(site.getusersitepackages())"], env=env, text=True
            ).strip()
        )
        self.assertTrue(user_site.is_relative_to(self.home))
        user_site.mkdir(parents=True)
        markers = [self.home / "pth-ran", self.home / "usercustomize-ran"]
        for file, marker in zip(("planted.pth", "usercustomize.py"), markers):
            (user_site / file).write_text("import pathlib; pathlib.Path(" + repr(str(marker)) + ").touch()\n")
        subprocess.run([tools["python3"], "-c", "pass"], env=env, check=True)
        self.assertTrue(all(path.exists() for path in markers))
        for path in markers:
            path.unlink()
        result = subprocess.run(command, shell=True, input=payload, text=True, capture_output=True, env=env, cwd=anchor)
        self.assertEqual(result.returncode, 0, result.stderr)
        decision = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual((decision["hookEventName"], decision["decision"]["behavior"]), ("PermissionRequest", "allow"))
        self.assertFalse(any(path.exists() for path in markers))
        self.assertTrue(guard.read_text().startswith("#!/bin/bash\n"))
        self.assertTrue(all(Path(path).is_absolute() and os.access(path, os.X_OK) for path in policy["tools"].values()))
        worker = expand(self.module.render_claude_worker_settings(self.manifest), self.home)
        for hook in [
            *all_hooks(settings),
            *all_hooks(worker),
            *all_hooks(json.loads((ROOT / ".claude/settings.json").read_text())),
        ]:
            expanded = (
                hook["command"]
                .replace("${CLAUDE_PROJECT_DIR}", str(anchor))
                .replace("${CLAUDE_ENV_FILE}", env["CLAUDE_ENV_FILE"])
                .replace("$HOME", str(self.home))
                .replace("${HERDR_PANE_ID}", "fixture-pane")
            )
            words = shlex.split(expanded)
            for executable in (words[0], next(word for word in words[2:] if "=" not in word)):
                self.assertTrue(
                    Path(executable).is_absolute() and Path(executable).is_file() and os.access(executable, os.X_OK),
                    executable,
                )
            result = subprocess.run(
                expanded,
                shell=True,
                input=payload
                if hook["command"] == command
                else json.dumps({"tool_input": {"file_path": str(anchor / "source.py")}}),
                env=env,
                cwd=anchor,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(any(path.exists() for path in markers))

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
