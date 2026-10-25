"""Exercise setup-gh with a fake gh and gh-auth.sh: one login path, key scopes off the machine login."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_setup-gh"
# The fake gh logs each call with the config directory it saw; `auth login` fails when FAIL_LOGIN is set.
FAKE_GH = """#!/bin/sh
printf '%s|%s\\n' "${GH_CONFIG_DIR-default}" "$*" >> "$GH_CALLS"
case "$1 $2" in
"auth login") [ -z "${FAIL_LOGIN-}" ] || exit 1; [ -d "$GH_CONFIG_DIR" ] && : > "$GH_CONFIG_DIR/hosts.yml" ;;
esac
exit 0
"""
FAKE_GH_AUTH = """#!/bin/sh
printf 'default|gh-auth.sh\\n' >> "$GH_CALLS"
"""


class SetupGhTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="setup-gh-test-"))
        self.home = self.temp / "home"
        (self.home / ".ssh").mkdir(parents=True)
        (self.home / ".ssh/id_ed25519.pub").write_text("ssh-ed25519 AAAA fixture\n")
        bin_dir = self.temp / "bin"
        bin_dir.mkdir()
        for name, body in (("gh", FAKE_GH), ("gh-auth.sh", FAKE_GH_AUTH)):
            (bin_dir / name).write_text(body)
            (bin_dir / name).chmod(0o755)
        self.tmpdir = self.temp / "tmp"
        self.tmpdir.mkdir()
        self.calls = self.temp / "calls"
        self.env = {
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "HOME": str(self.home),
            "TMPDIR": str(self.tmpdir),
            "GH_CALLS": str(self.calls),
            "DOTFILES_GH_AUTH_SCRIPT": str(bin_dir / "gh-auth.sh"),
        }

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def run_setup_gh(self, **extra: str) -> tuple[subprocess.CompletedProcess, list[tuple[str, str]]]:
        result = subprocess.run(
            ["bash", str(SCRIPT)],
            stdin=subprocess.DEVNULL,
            env={**self.env, **extra},
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        lines = self.calls.read_text().splitlines() if self.calls.exists() else []
        return result, [tuple(line.split("|", 1)) for line in lines]

    def test_machine_login_goes_through_gh_auth_and_never_gains_key_scopes(self):
        result, calls = self.run_setup_gh()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(("default", "gh-auth.sh"), calls[0])
        default_calls = [command for config, command in calls if config == "default"]
        self.assertEqual(["gh-auth.sh"], default_calls)
        key_configs = {config for config, _ in calls[1:]}
        self.assertEqual(1, len(key_configs))
        key_config = key_configs.pop()
        commands = [command for _, command in calls[1:]]
        self.assertIn("admin:public_key,admin:ssh_signing_key", commands[0])
        self.assertTrue(commands[0].startswith("auth login "))
        self.assertIn("ssh-key add", commands[1])
        self.assertIn("--type authentication", commands[1])
        self.assertIn("--type signing", commands[2])
        self.assertTrue(commands[3].startswith("auth logout"))
        self.assertFalse(Path(key_config).exists())
        self.assertFalse(any("auth refresh" in command for _, command in calls))

    def test_failed_one_off_login_uploads_nothing_and_removes_its_config(self):
        result, calls = self.run_setup_gh(FAIL_LOGIN="1")
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(any("ssh-key add" in command for _, command in calls))
        self.assertEqual([], list(self.tmpdir.iterdir()))

    def test_missing_gh_auth_script_stops_before_any_gh_call(self):
        result, calls = self.run_setup_gh(DOTFILES_GH_AUTH_SCRIPT=str(self.temp / "absent.sh"))
        self.assertEqual(1, result.returncode)
        self.assertIn("make gh-auth", result.stderr)
        self.assertEqual([], calls)


if __name__ == "__main__":
    unittest.main()
