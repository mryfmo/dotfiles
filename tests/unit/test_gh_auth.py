"""Exercise scripts/gh-auth.sh (one GitHub login per machine) with a fake gh."""

from __future__ import annotations

import os
import pty
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/gh-auth.sh"
LOGIN = "auth login --hostname github.com --git-protocol https --insecure-storage"
STATUS = (
    "auth status --hostname github.com --active --json hosts"
    """ --jq .hosts["github.com"][] | select(.state == "success") | .tokenSource"""
)
# The fake gh logs each call with the token it saw. `auth status` prints the working login's token
# source from the login marker (as the real --jq does), and `auth login` writes a 0644 hosts.yml.
FAKE_GH = """#!/bin/sh
printf '%s|%s\\n' "${GH_TOKEN-unset}" "$*" >> "$GH_CALLS"
case "$1 $2" in
"auth status") [ ! -f "$HOME/.gh-login" ] || cat "$HOME/.gh-login" ;;
"auth login")
  [ -z "${FAIL_LOGIN-}" ] || exit 1
  mkdir -p "$HOME/.config/gh" && : > "$HOME/.config/gh/hosts.yml" && chmod 644 "$HOME/.config/gh/hosts.yml"
  echo "$HOME/.config/gh/hosts.yml" > "$HOME/.gh-login" ;;
*) exit 2 ;;
esac
"""


class GhAuthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="gh-auth-test-"))
        self.home = self.temp / "home"
        self.home.mkdir()
        self.bin_dir = self.temp / "bin"
        self.bin_dir.mkdir()
        (self.bin_dir / "gh").write_text(FAKE_GH)
        (self.bin_dir / "gh").chmod(0o755)
        self.calls = self.temp / "calls"
        self.hosts = self.home / ".config/gh/hosts.yml"
        self.env = {
            "PATH": f"{self.bin_dir}:/usr/bin:/bin",
            "HOME": str(self.home),
            "GH_CALLS": str(self.calls),
            "GH_TOKEN": "fixture-env-token",
        }

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def run_command(self, command: list[str], stdin, env: dict | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            command, stdin=stdin, env=env or self.env, capture_output=True, text=True, check=False, timeout=30
        )

    def on_a_terminal(self, command: list[str], env: dict | None = None) -> subprocess.CompletedProcess:
        primary, secondary = pty.openpty()
        try:
            return self.run_command(command, secondary, env)
        finally:
            os.close(primary)
            os.close(secondary)

    def logged_calls(self) -> list[str]:
        return self.calls.read_text().splitlines() if self.calls.exists() else []

    def install_setup_copy(self) -> None:
        script = self.home / ".local/share/chezmoi/scripts/gh-auth.sh"
        script.parent.mkdir(parents=True)
        shutil.copy(SCRIPT, script)

    def hosts_mode(self) -> int:
        return self.hosts.stat().st_mode & 0o777

    def test_a_working_file_login_is_left_alone_but_set_to_0600(self) -> None:
        self.hosts.parent.mkdir(parents=True)
        self.hosts.touch(mode=0o644)
        self.hosts.chmod(0o644)
        (self.home / ".gh-login").write_text(f"{self.hosts}\n")

        result = self.run_command([str(SCRIPT)], subprocess.DEVNULL)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("gh already holds a working login; skipped", result.stdout)
        self.assertEqual(self.logged_calls(), [f"unset|{STATUS}"])
        self.assertEqual(self.hosts_mode(), 0o600)

    def test_a_working_keyring_login_is_moved_to_the_file(self) -> None:
        # The sandbox cannot reach the keyring, so a keyring login counts as none.
        (self.home / ".gh-login").write_text("keyring\n")

        headless = self.run_command([str(SCRIPT)], subprocess.DEVNULL)
        terminal = self.on_a_terminal([str(SCRIPT)])

        self.assertEqual(headless.returncode, 1)
        self.assertIn("gh's working login is in the OS keyring, which the Claude sandbox cannot reach", headless.stderr)
        self.assertEqual(terminal.returncode, 0, terminal.stderr)
        self.assertEqual(self.logged_calls(), [f"unset|{STATUS}", f"unset|{STATUS}", f"unset|{LOGIN}"])
        self.assertEqual(self.hosts_mode(), 0o600)

    def test_without_a_terminal_it_never_prompts(self) -> None:
        result = self.run_command([str(SCRIPT)], subprocess.DEVNULL)

        self.assertEqual(result.returncode, 1)
        self.assertIn('gh holds no working login; run "make gh-auth" in a terminal', result.stderr)
        self.assertEqual(self.logged_calls(), [f"unset|{STATUS}"])

    def test_on_a_terminal_it_logs_in_to_gh_file_at_0600(self) -> None:
        result = self.on_a_terminal([str(SCRIPT)])

        self.assertEqual(result.returncode, 0, result.stderr)
        # File storage (--insecure-storage), and the token env is cleared.
        self.assertEqual(self.logged_calls(), [f"unset|{STATUS}", f"unset|{LOGIN}"])
        self.assertEqual(self.hosts_mode(), 0o600)

    def test_a_failing_chmod_fails_the_step(self) -> None:
        (self.bin_dir / "chmod").write_text("#!/bin/sh\nexit 1\n")
        (self.bin_dir / "chmod").chmod(0o755)

        result = self.on_a_terminal([str(SCRIPT)])

        self.assertEqual(result.returncode, 1)
        self.assertIn(f"cannot set {self.hosts.parent}/hosts.yml to mode 0600", result.stderr)

    def test_a_login_that_does_not_complete_fails(self) -> None:
        self.install_setup_copy()
        env = {**self.env, "FAIL_LOGIN": "1"}

        direct = self.on_a_terminal([str(SCRIPT)], env)
        setup = self.on_a_terminal(["bash", "-c", f'source "{ROOT}/setup.sh"; authenticate_github'], env)

        self.assertEqual(direct.returncode, 1)
        # setup.sh reports it and carries on: the bootstrap itself already succeeded.
        self.assertEqual(setup.returncode, 0, setup.stderr)
        self.assertIn("The GitHub login did not complete; run `make gh-auth` to retry.", setup.stderr)

    def test_a_missing_gh_is_reported(self) -> None:
        # A PATH with bash alone: CI runners and most hosts have a real gh in /usr/bin.
        bash_only = self.temp / "bash-only"
        bash_only.mkdir()
        (bash_only / "bash").symlink_to(shutil.which("bash"))
        result = self.run_command([str(SCRIPT)], subprocess.DEVNULL, {**self.env, "PATH": str(bash_only)})

        self.assertEqual(result.returncode, 1)
        self.assertIn('gh is not installed; install it, then run "make gh-auth"', result.stderr)

    def test_setup_skips_the_login_in_ci_without_calling_gh(self) -> None:
        # The public-bootstrap CI jobs run setup.sh with CI=true and no terminal: nothing may prompt.
        self.install_setup_copy()

        result = self.run_command(
            ["bash", "-c", f'source "{ROOT}/setup.sh"; authenticate_github'],
            subprocess.DEVNULL,
            {**self.env, "CI": "true"},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Skipping the GitHub login; run `make gh-auth`", result.stdout)
        self.assertEqual(self.logged_calls(), [])

    def test_setup_finds_a_mise_installed_gh_on_a_fresh_path(self) -> None:
        # A fresh bootstrap shell has no mise shims on PATH; gh exists only as a shim.
        shims = self.home / ".local/share/mise/shims"
        shims.mkdir(parents=True)
        shutil.copy(self.bin_dir / "gh", shims / "gh")
        self.install_setup_copy()

        result = self.on_a_terminal(
            ["bash", "-c", f'source "{ROOT}/setup.sh"; authenticate_github'], {**self.env, "PATH": "/usr/bin:/bin"}
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Skipping the GitHub login", result.stdout)
        self.assertEqual(self.logged_calls(), [f"unset|{STATUS}", f"unset|{LOGIN}"])


if __name__ == "__main__":
    unittest.main()
