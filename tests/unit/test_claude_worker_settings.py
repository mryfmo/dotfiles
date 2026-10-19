"""Check worker configuration and execute guarded fixture hook commands."""

import base64
import fnmatch
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import unittest

from tests.unit.test_generate_agent_configs import (
    ROOT,
    all_hooks,
    load_generator,
    load_manifest_fixture,
    render_claude_template,
)


def expand(text, home, os_name="darwin"):
    text = re.sub(
        r'{{ if eq \.chezmoi\.os "darwin" }}(.*?){{ else }}(.*?){{ end }}',
        lambda m: m[1] if os_name == "darwin" else m[2],
        text,
        flags=re.S,
    )
    return json.loads(text.replace("{{ .chezmoi.homeDir }}", str(home)))


def run_hook(command, root, data="{}", **extra_env):
    return subprocess.run(
        command,
        shell=True,
        input=data,
        text=True,
        capture_output=True,
        env=dict(os.environ, CLAUDE_PROJECT_DIR=str(root), **extra_env),
    )


class ClaudeWorkerSettingsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / "home with spaces"
        self.home.mkdir()
        self.module = load_generator()
        self.manifest = json.loads(
            json.dumps(load_manifest_fixture(self.home)).replace("/render-home", "{{ .chezmoi.homeDir }}")
        )
        template = self.home / "source/.chezmoitemplates/claude-worker-settings.json"
        template.parent.mkdir(parents=True)
        template.write_text(self.module.render_claude_worker_settings(self.manifest))

    def modify(self, text):
        return subprocess.run(
            [sys.executable, "-I", str(ROOT / "home/dot_claude-worker/modify_private_settings.json")],
            input=text,
            text=True,
            capture_output=True,
            env=dict(os.environ, CHEZMOI_HOME_DIR=str(self.home), CHEZMOI_SOURCE_DIR=str(self.home / "source")),
        )

    def settings(self, os_name="darwin"):
        return expand(self.module.render_claude_worker_settings(self.manifest), self.home, os_name)

    def run_guard(self, *args, **kwargs):
        return run_hook(*args, HOME=str(self.home), **kwargs)

    def test_guard_template_binds_each_home_without_changing_tracked_commands(self):
        tracked = (ROOT / ".claude/settings.json").read_text()
        source = (ROOT / "home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl").read_text()
        for name in ("host one", "host two", "host 'quoted'"):
            home = self.home / name
            anchor = home / "anchor"
            anchor.mkdir(parents=True)
            manifest = json.loads(json.dumps(self.manifest))
            manifest["claude"]["orchestrator_checkout"] = str(anchor)
            text = self.module.render_orchestrator_guard(manifest, source)
            rendered = render_claude_template(text, home, home=str(home), raw=True)
            policy = json.loads(
                base64.b64decode(
                    shlex.split(next(line[7:] for line in rendered.splitlines() if line.startswith("policy=")))[0]
                )
            )
            rendered_home = base64.b64decode(
                shlex.split(next(line[5:] for line in rendered.splitlines() if line.startswith("home=")))[0]
            ).decode()
            self.assertEqual(rendered_home, str(home))
            self.assertEqual(policy["root"], str(anchor))
            self.assertNotIn("{{ output", rendered)
            self.assertEqual(tracked, (ROOT / ".claude/settings.json").read_text())

    def guard_command(self, anchor, argv, mode="project"):
        original = (ROOT / "home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl").read_text()
        policy = {
            "root": str(anchor),
            "commands": {"fixture": {"argv": argv, "mode": mode}},
        }
        block = (
            "home="
            + base64.b64encode(str(self.home).encode()).decode()
            + "\npolicy="
            + base64.b64encode(json.dumps(policy).encode()).decode()
        )
        text, count = re.subn(
            r"(?<=# BEGIN TRUSTED POLICY\n).*?(?=\n# END TRUSTED POLICY)", lambda _: block, original, flags=re.S
        )
        self.assertEqual(count, 1, "missing rendered policy binding block")
        guard = self.home / ".claude/hooks/orchestrator-only.sh"
        guard.parent.mkdir(parents=True, exist_ok=True)
        guard.write_text(text)
        guard.chmod(0o755)
        return self.module.HOOK_PREFIX + '"$HOME/.claude/hooks/orchestrator-only.sh" fixture'

    def test_worker_policy_renders_for_both_platforms(self):
        for platform in ("darwin", "linux"):
            settings = self.settings(platform)
            self.assertEqual(settings["permissions"]["defaultMode"], "auto")
            checkout_rules = [r for r in settings["permissions"]["deny"] if "/Workspace/dotfiles/" in r]
            self.assertTrue(checkout_rules and all(r.startswith("Edit(//") for r in checkout_rules))
            sandbox = settings["sandbox"]
            self.assertTrue(sandbox["enabled"] and sandbox["failIfUnavailable"])
            self.assertFalse(sandbox["allowUnsandboxedCommands"])
            self.assertEqual(sandbox["excludedCommands"], [])
            self.assertNotIn("allowUnixSockets", sandbox["network"])
            self.assertNotIn("allowAllUnixSockets", sandbox["network"])
            self.assertEqual(
                sandbox["filesystem"]["allowWrite"],
                [str(self.home / ".agents/skills/agmsg" / part) for part in ("db", "teams", "run", "ext-tools")],
            )
            self.assertIn("Bash(gh pr merge:*)", settings["permissions"]["deny"])
            self.assertFalse(settings["enableAllProjectMcpServers"])
            self.assertEqual(settings["enabledMcpjsonServers"], [])
            self.assertFalse(settings["syncClaudeAiPlugins"] or settings["syncClaudeAiSkills"])
            self.assertTrue(settings["enabledPlugins"])
            self.assertTrue(all(value is False for value in settings["enabledPlugins"].values()))
            self.assertIn("crit@skills-dir", settings["enabledPlugins"])

    def test_worker_denies_leave_agmsg_stores_writable(self):
        patterns = [p[5:-1] for p in self.settings()["permissions"]["deny"] if p.startswith("Edit(")]
        self.assertIn("~/.agents/skills/agmsg/plugins/**", patterns)
        self.assertIn("~/.agents/skills/agmsg/db/trusted-plugins", patterns)
        for part in ("db", "teams", "run", "ext-tools"):
            for suffix in ("", "/fixture", "/nested/fixture"):
                path = "~/.agents/skills/agmsg/" + part + suffix
                self.assertFalse(any(fnmatch.fnmatchcase(path, p) for p in patterns), path)
        self.assertFalse(any(p in patterns for p in ("~/.agents/**", "~/.local/**")))

    def test_worker_denies_protect_permgate_policy(self):
        policy = self.home / ".agents/permgate-policy.yaml"
        policy.parent.mkdir(parents=True, exist_ok=True)
        policy.write_bytes(b"trusted-policy\n")
        for tool in ("Edit", "Write"):
            patterns = [rule[5:-1] for rule in self.settings()["permissions"]["deny"] if rule.startswith("Edit(")]
            denied = any(fnmatch.fnmatchcase("~/.agents/permgate-policy.yaml", pattern) for pattern in patterns)
            self.assertTrue(denied, tool)
            if not denied:
                policy.write_bytes(b"worker-change\n")
            self.assertEqual(policy.read_bytes(), b"trusted-policy\n")

    def test_worker_settings_replace_stale_policy_idempotently(self):
        stale = json.dumps(
            {
                "sandbox": {"enabled": False, "excludedCommands": ["*"]},
                "permissions": {"allow": ["Bash(*)"]},
                "hooks": {"Stop": [{"command": "stale"}]},
                "unrelated": 1,
            }
        )
        for initial in (stale, "", "{broken"):
            result = self.modify(initial)
            self.assertEqual(result.returncode, 0, result.stderr)
            desired = json.loads(result.stdout)
            for key in self.settings():
                self.assertEqual(desired[key], self.settings()[key])
            again = self.modify(result.stdout)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(again.stdout, result.stdout)

    def test_worker_settings_do_not_import_orchestrator_hooks(self):
        orchestrator = self.home / ".claude/settings.json"
        orchestrator.parent.mkdir()
        orchestrator.write_text(
            json.dumps(
                {
                    "enabledPlugins": {"poison-plugin": True},
                    "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "poison-hook"}]}]},
                }
            )
        )
        result = self.modify("{}")
        self.assertEqual(result.returncode, 0, result.stderr)
        settings = json.loads(result.stdout)
        self.assertNotIn("poison", result.stdout)
        self.assertTrue(all(value is False for value in settings["enabledPlugins"].values()))
        text = json.dumps(settings["hooks"])
        for name in ("format-edited", "project-map", "permgate", "herdr-agent-state", "--attach"):
            self.assertNotIn(name, text)
        self.assertEqual(set(settings["hooks"]), {"SessionStart", "SessionEnd", "Stop"})
        for hook in all_hooks(settings):
            self.assertEqual(hook["onFailure"], "block")
            self.assertTrue(hook["command"].startswith("/usr/bin/env -i PATH=/usr/bin:/bin HOME="))
            self.assertIn("AGMSG_RESOLVE_PROJECT=0", hook["command"])

    def test_project_guard_uses_launch_root_and_never_runs_worker_payloads(self):
        anchor = self.home / "checkout"
        worker = anchor / ".claude/worktrees/worker"
        worker.mkdir(parents=True)
        (worker / ".prettierrc.cjs").write_text("throw new Error('worker config executed')")
        (worker / "ruff.toml").write_text("deliberately invalid TOML")
        marker = self.home / "payload.json"
        for name in (
            "scripts/agent-stop-gate.sh",
            ".claude/hooks/contextdb_hook.py",
            ".claude/hooks/contextdb_recover.py",
        ):
            target = worker / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("raise SystemExit('worker project payload executed')\n")
        poison = self.home / "bash-env"
        poison.write_text(f"touch {shlex.quote(str(self.home / 'poisoned'))}\n")
        payload = self.home / "payload.py"
        payload.write_text(
            "import json,os,sys\nfrom pathlib import Path\n"
            "Path(sys.argv[1]).write_text(json.dumps([sys.argv[2:],sys.stdin.read(),os.environ['PATH']]))\n"
            "raise SystemExit(7)\n"
        )
        argv = ["/usr/bin/python3", "-I", str(payload), str(marker), "arg with spaces"]
        command = self.guard_command(anchor, argv)
        for root in (str(worker), str(self.home), "", str(anchor / "missing")):
            result = self.run_guard(command, root, json.dumps({"cwd": str(anchor)}), BASH_ENV=str(poison))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())
        for hook in all_hooks(json.loads((ROOT / ".claude/settings.json").read_text())):
            self.assertEqual(self.run_guard(hook["command"], worker).returncode, 0)
        alias = self.home / "anchor-alias"
        alias.symlink_to(anchor, target_is_directory=True)
        result = self.run_guard(command, alias, "unchanged stdin", BASH_ENV=str(poison))
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertEqual(json.loads(marker.read_text())[:2], [["arg with spaces"], "unchanged stdin"])
        self.assertFalse((self.home / "poisoned").exists())
        for mode in ("format", "project-map"):
            edited = anchor / "file.md"
            edited.write_text("fixture")
            for file in (worker / "file.md", self.home / "outside.md", edited):
                marker.unlink(missing_ok=True)
                line = self.guard_command(anchor, argv, mode)
                event = json.dumps({"tool_input": {"file_path": str(file)}})
                result = self.run_guard(line, anchor, event)
                self.assertEqual(marker.exists(), file == edited, result.stderr)
                self.assertEqual(result.returncode, 7 if file == edited else 0, result.stderr)
            alias = Path(str(edited).swapcase())
            if alias.exists() and alias.samefile(edited):
                result = self.run_guard(
                    line, Path(str(anchor).swapcase()), json.dumps({"tool_input": {"file_path": str(alias)}})
                )
                self.assertEqual(result.returncode, 7, result.stderr)


if __name__ == "__main__":
    unittest.main()
