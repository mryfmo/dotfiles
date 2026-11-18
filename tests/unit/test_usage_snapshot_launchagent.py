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
PLIST_HASH = '{{ includeTemplate "Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl" . | sha256sum }}'
DEST_DIR = "{{ .chezmoi.destDir | replace \"'\" \"'\\\\''\" }}"
MISSING_DOMAIN = "Bad request.\nCould not find domain for user gui: 99999"


def rendered(dest_dir: str) -> str:
    """The script as chezmoi renders it on macOS for an apply into `dest_dir`: the darwin guard dropped, the includes
    and the destination in place, the plist hash a constant."""
    lines = [
        line
        for line in SCRIPT.read_text().splitlines(keepends=True)
        if not re.fullmatch(r"\{\{ (if .*|end) -\}\}\n", line)
    ]
    body = "".join(lines)
    return body.replace(LIB_INCLUDE, LIB.read_text()).replace(PLIST_HASH, "0" * 64).replace(DEST_DIR, dest_dir)


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
            "    print)\n"
            '        if [ -n "${FAKE_PRINT_RC:-}" ]; then echo "Operation not permitted" >&2; exit "${FAKE_PRINT_RC}"; fi\n'
            '        if [ "${FAKE_DOMAIN_PRESENT:-1}" = 1 ]; then echo "{ listed }"; exit 0; fi\n'
            f'        printf "%s\\n" "{MISSING_DOMAIN}" >&2; exit 113 ;;\n'
            '    bootout) exit "${FAKE_BOOTOUT_RC:-0}" ;;\n'
            '    bootstrap) [ "${FAKE_BOOTSTRAP_RC:-0}" = 0 ] || echo "Bootstrap failed: 5: Input/output error" >&2; exit "${FAKE_BOOTSTRAP_RC:-0}" ;;\n'
            "esac\n"
            "exit 64\n"
        )
        (self.fake / "launchctl").chmod(0o755)
        self.script = self.temp / "reload.sh"
        self.script.write_text(rendered(str(self.home)))
        self.uid = subprocess.run(["id", "-u"], capture_output=True, text=True, check=True).stdout.strip()

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

    def test_the_template_embeds_the_rendered_plist_and_no_host_path(self) -> None:
        text = SCRIPT.read_text()
        self.assertIn('{{ if eq .chezmoi.os "darwin" -}}', text)
        self.assertIn(LIB_INCLUDE, text)
        self.assertIn(PLIST_HASH, text, "the plist as rendered for this host, so its tree, home and text all count")
        self.assertIn(DEST_DIR, text, "the destination is compared, single-quoted, never interpolated")
        self.assertNotIn(".chezmoi.workingTree", text, "no host path is written into the script")
        self.assertNotIn(".chezmoi.homeDir", text)
        for name in (".chezmoi.workingTree", ".chezmoi.homeDir"):
            self.assertIn(name, PLIST.read_text(), f"the plist renders {name}, which the hash covers")
        self.assertTrue(SCRIPT.name.startswith("run_onchange_after_"), "runs on a content change, not once")

    def test_a_present_domain_and_plist_reload_the_agent(self) -> None:
        plist = self.place_plist()
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            [f"print gui/{self.uid}", f"bootout gui/{self.uid}/{LABEL}", f"bootstrap gui/{self.uid} {plist}"],
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

    def test_a_missing_user_domain_skips_with_one_line(self) -> None:
        self.place_plist()
        result = self.run_script(FAKE_DOMAIN_PRESENT="0")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([f"print gui/{self.uid}"], self.calls(), "the domain probe alone")
        self.assertEqual(f"No user launchd domain gui/{self.uid}; skipping {LABEL} reload.\n", result.stderr)
        self.assertEqual("", result.stdout)

    def test_a_failed_domain_probe_is_a_failure_not_an_absence(self) -> None:
        self.place_plist()
        result = self.run_script(FAKE_PRINT_RC="1")
        self.assertEqual(1, result.returncode)
        self.assertEqual([f"print gui/{self.uid}"], self.calls(), "nothing unloaded or loaded")
        self.assertEqual(
            f"launchctl print gui/{self.uid} failed with status 1: Operation not permitted\n", result.stderr
        )
        self.assertEqual("", result.stdout)

    def test_a_failed_uid_read_fails_before_any_launchctl_call(self) -> None:
        self.place_plist()
        (self.fake / "id").write_text("#!/bin/bash\nexit 7\n")
        (self.fake / "id").chmod(0o755)
        result = self.run_script()
        self.assertEqual(7, result.returncode)
        self.assertEqual([], self.calls())
        self.assertNotIn("reloaded", result.stdout)

    def test_a_destination_other_than_home_skips_with_one_line(self) -> None:
        self.place_plist()
        elsewhere = self.temp / "dest"
        elsewhere.mkdir()
        self.script.write_text(rendered(str(elsewhere)))
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], self.calls(), "the live plist under HOME is not touched for an apply elsewhere")
        self.assertEqual(
            f"The destination is not the home directory (temp destDir apply?); skipping {LABEL} reload.\n",
            result.stderr,
        )

    def test_a_destination_with_a_quote_or_newline_in_its_name_is_compared_not_run(self) -> None:
        self.place_plist()
        odd = self.temp / "it's\nodd"
        odd.mkdir()
        marker = self.temp / "ran"
        hostile = f"{odd}'; touch {marker}; echo '"
        self.script.write_text(rendered(hostile.replace("'", "'\\''")))
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(marker.exists(), "the destination text stays inside its quotes")
        self.assertEqual([], self.calls())

    def test_a_plist_not_visible_under_home_skips_with_one_line(self) -> None:
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([f"print gui/{self.uid}"], self.calls(), "the domain probe alone; nothing bootstrapped")
        self.assertIn("not visible (temp destDir apply?); skipping", result.stderr)

    def test_a_github_actions_runner_runs_nothing_and_says_so(self) -> None:
        self.place_plist()
        result = self.run_script(GITHUB_ACTIONS="true", RUNNER_TEMP=str(self.temp))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], self.calls())
        self.assertEqual(("", f"GitHub Actions runner; skipping {LABEL} reload.\n"), (result.stdout, result.stderr))

    def test_an_agent_shell_s_ci_variable_is_not_a_runner(self) -> None:
        plist = self.place_plist()
        result = self.run_script(CI="true")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(3, len(self.calls()))
        self.assertIn(str(plist), self.calls()[-1])


if __name__ == "__main__":
    unittest.main()
