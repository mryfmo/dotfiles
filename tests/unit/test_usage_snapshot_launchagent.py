"""The usage-snapshot LaunchAgent is reloaded when its rendered plist changes (regime-cutover U585)."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/.chezmoiscripts/macos/run_onchange_after_60-reload-usage-snapshot-agent.sh.tmpl"
PLIST = ROOT / "home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl"
LIB = ROOT / "scripts/lib/ci-runner.sh"
LABEL = "com.mryfmo.dotfiles.usage-snapshot"
LIB_INCLUDE = '{{ include "../scripts/lib/ci-runner.sh" }}'
PLIST_INCLUDE = '{{ include "Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl" | sha256sum }}'
WORKING_TREE = "{{ .chezmoi.workingTree }}"


def rendered(working_tree: str = "/tree") -> str:
    """The script as chezmoi renders it on macOS: the darwin guard dropped, the includes and the tree in place."""
    text = SCRIPT.read_text()
    lines = [line for line in text.splitlines(keepends=True) if not re.fullmatch(r"\{\{ (if .*|end) -\}\}\n", line)]
    body = "".join(lines)
    return body.replace(LIB_INCLUDE, LIB.read_text()).replace(PLIST_INCLUDE, "0" * 64).replace(WORKING_TREE, working_tree)


class UsageSnapshotLaunchAgentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="usage-snapshot-agent-test-"))
        self.home = self.temp / "home"
        self.home.mkdir()
        self.log = self.temp / "launchctl.log"
        self.fake = self.temp / "bin"
        self.fake.mkdir()
        (self.fake / "launchctl").write_text(
            "#!/bin/bash\n"
            f'printf "%s\\n" "$*" >> "{self.log}"\n'
            'case "$1" in\n'
            '    print) [ "${FAKE_DOMAIN_PRESENT:-1}" = 1 ] && exit 0 || exit 113 ;;\n'
            '    bootout) exit "${FAKE_BOOTOUT_RC:-0}" ;;\n'
            '    bootstrap) [ "${FAKE_BOOTSTRAP_RC:-0}" = 0 ] || echo "Bootstrap failed: 5: Input/output error" >&2; exit "${FAKE_BOOTSTRAP_RC:-0}" ;;\n'
            "esac\n"
            "exit 64\n"
        )
        (self.fake / "launchctl").chmod(0o755)
        self.script = self.temp / "reload.sh"
        self.script.write_text(rendered())

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def run_script(self, **env: str) -> subprocess.CompletedProcess:
        base = {"PATH": f"{self.fake}:/usr/bin:/bin", "HOME": str(self.home)}
        return subprocess.run(
            ["bash", str(self.script)], env=base | env, capture_output=True, text=True, check=False, timeout=30
        )

    def calls(self) -> list[str]:
        return self.log.read_text().splitlines() if self.log.exists() else []

    def place_plist(self) -> Path:
        plist = self.home / "Library/LaunchAgents" / f"{LABEL}.plist"
        plist.parent.mkdir(parents=True)
        plist.write_text("<plist/>\n")
        return plist

    def test_the_template_embeds_what_the_plist_renders_from(self) -> None:
        text = SCRIPT.read_text()
        self.assertIn('{{ if eq .chezmoi.os "darwin" -}}', text)
        self.assertIn(LIB_INCLUDE, text)
        self.assertIn(PLIST_INCLUDE, text, "an edit to the plist template re-renders this script")
        self.assertIn(WORKING_TREE, text, "a moved source clone re-renders this script (the plist names the tree)")
        self.assertIn("{{ .chezmoi.workingTree }}", PLIST.read_text(), "the plist does name the tree")
        self.assertTrue(SCRIPT.name.startswith("run_onchange_after_"), "runs on a content change, not once")

    def test_a_present_domain_and_plist_reload_the_agent(self) -> None:
        plist = self.place_plist()
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        uid = subprocess.run(["id", "-u"], capture_output=True, text=True, check=True).stdout.strip()
        self.assertEqual(
            [f"print gui/{uid}", f"bootout gui/{uid}/{LABEL}", f"bootstrap gui/{uid} {plist}"],
            self.calls(),
        )
        self.assertEqual(f"{LABEL} reloaded from {plist}.\n", result.stdout)
        self.assertEqual("", result.stderr)

    def test_an_agent_launchd_does_not_hold_is_still_loaded(self) -> None:
        self.place_plist()
        result = self.run_script(FAKE_BOOTOUT_RC="113")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(3, len(self.calls()))
        self.assertIn("reloaded", result.stdout)

    def test_a_refused_bootstrap_fails_the_apply_with_launchd_s_words(self) -> None:
        self.place_plist()
        result = self.run_script(FAKE_BOOTSTRAP_RC="5")
        self.assertEqual(5, result.returncode)
        self.assertIn("Bootstrap failed", result.stderr)
        self.assertNotIn("reloaded", result.stdout)

    def test_no_user_domain_skips_with_one_line(self) -> None:
        self.place_plist()
        result = self.run_script(FAKE_DOMAIN_PRESENT="0")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(1, len(self.calls()), "the domain probe alone")
        self.assertRegex(result.stderr, r"^No user launchd domain gui/\d+; skipping .* reload\.\n$")
        self.assertEqual("", result.stdout)

    def test_a_plist_not_visible_under_home_skips_with_one_line(self) -> None:
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(1, len(self.calls()), "the domain probe alone; nothing bootstrapped")
        self.assertIn("not visible (temp destDir apply?); skipping", result.stderr)

    def test_a_github_actions_runner_runs_nothing(self) -> None:
        self.place_plist()
        result = self.run_script(GITHUB_ACTIONS="true", RUNNER_TEMP=str(self.temp))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], self.calls())
        self.assertEqual(("", ""), (result.stdout, result.stderr))

    def test_an_agent_shell_s_ci_variable_is_not_a_runner(self) -> None:
        plist = self.place_plist()
        result = self.run_script(CI="true")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(3, len(self.calls()))
        self.assertIn(str(plist), self.calls()[-1])


if __name__ == "__main__":
    unittest.main()
