"""Exercise scripts/gh-auth-stores.sh with a fake gh."""

from __future__ import annotations

import os
import pty
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/gh-auth-stores.sh"
# The fake gh logs each call with its store, succeeds `auth status` only for a store holding a
# token marker, and `auth login` writes that marker into a group-readable hosts.yml.
FAKE_GH = """#!/bin/sh
printf '%s|%s|%s\\n' "$GH_CONFIG_DIR" "${GH_TOKEN-unset}" "$*" >> "$GH_CALLS"
case "$1 $2" in
"auth status") [ -f "$GH_CONFIG_DIR/token" ] ;;
"auth login") : > "$GH_CONFIG_DIR/token"; : > "$GH_CONFIG_DIR/hosts.yml"; chmod 644 "$GH_CONFIG_DIR/hosts.yml" ;;
"auth setup-git") ;;
*) exit 2 ;;
esac
"""


class GhAuthStoresTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="gh-auth-stores-test-"))
        self.home = self.temp / "home"
        bin_dir = self.temp / "bin"
        bin_dir.mkdir()
        (bin_dir / "gh").write_text(FAKE_GH)
        (bin_dir / "gh").chmod(0o755)
        self.calls = self.temp / "calls"
        self.env_file = self.temp / "model-profiles.env"
        self.env_file.write_text(
            "OWNER_GH_CONFIG_DIR='~/.config/gh'\n"
            "WORK_GH_CONFIG_DIR='~/.config/gh-work'\n"
            f"WORKER_GH_CONFIG_DIR='{self.temp}/worker store'\n"
        )
        # The owner store is already populated (for example by chezmoi-private): no prompt for it.
        (self.home / ".config/gh").mkdir(parents=True)
        (self.home / ".config/gh/token").touch()
        self.env = {
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "HOME": str(self.home),
            "GH_CALLS": str(self.calls),
            "GH_AUTH_STORES_ENV": str(self.env_file),
            "GH_TOKEN": "fixture-env-token",
        }

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def run_script(self, stdin) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(SCRIPT)], stdin=stdin, env=self.env, capture_output=True, text=True, check=False, timeout=30
        )

    def logged_calls(self) -> list[str]:
        return self.calls.read_text().splitlines()

    def test_without_a_terminal_it_never_prompts(self) -> None:
        result = self.run_script(subprocess.DEVNULL)

        self.assertEqual(result.returncode, 1)
        self.assertIn(f"owner store {self.home}/.config/gh already holds a token; skipped", result.stdout)
        self.assertIn(f"work store {self.home}/.config/gh-work has no token; run", result.stderr)
        self.assertFalse(any("auth login" in call for call in self.logged_calls()))

    def test_setup_skips_the_logins_in_ci_without_calling_gh(self) -> None:
        # The public-bootstrap CI jobs run setup.sh with CI=true and no terminal: nothing may prompt.
        script = self.home / ".local/share/chezmoi/scripts/gh-auth-stores.sh"
        script.parent.mkdir(parents=True)
        shutil.copy(SCRIPT, script)
        result = subprocess.run(
            ["bash", "-c", f'source "{ROOT}/setup.sh"; authenticate_github'],
            stdin=subprocess.DEVNULL,
            env={**self.env, "CI": "true"},
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Skipping the GitHub logins; run `make gh-auth`", result.stdout)
        self.assertFalse(self.calls.exists())

    def test_on_a_terminal_it_logs_in_only_the_empty_stores(self) -> None:
        primary, secondary = pty.openpty()
        try:
            result = self.run_script(secondary)
        finally:
            os.close(primary)
            os.close(secondary)

        self.assertEqual(result.returncode, 0, result.stderr)
        work, worker = self.home / ".config/gh-work", self.temp / "worker store"
        login = "auth login --hostname github.com --git-protocol https --insecure-storage"
        setup_git = "auth setup-git --hostname github.com"
        self.assertEqual(
            self.logged_calls(),
            [
                f"{self.home}/.config/gh|unset|auth status --hostname github.com",
                f"{work}|unset|auth status --hostname github.com",
                f"{work}|unset|{login}",
                f"{work}|unset|{setup_git}",
                f"{worker}|unset|auth status --hostname github.com",
                f"{worker}|unset|{login}",
                f"{worker}|unset|{setup_git}",
            ],
        )
        for store in (work, worker):
            with self.subTest(store=store):
                self.assertEqual(stat.S_IMODE((store / "hosts.yml").stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(store.stat().st_mode), 0o700)


if __name__ == "__main__":
    unittest.main()
