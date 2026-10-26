"""Exercise setup-gh with a fake gh and gh-auth.sh: one login path, key scopes off the machine login."""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git  # noqa: E402

quiet_git()  # U100: no git command in this module's scratch repositories starts background maintenance

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_setup-gh"
# The fake gh logs each call with the config directory it saw; `auth login` fails when FAIL_LOGIN is set;
# `ssh-key add` touches $HANG_MARKER and hangs when that is set (an interrupt after authentication), and
# `auth logout` does the same with $HANG_LOGOUT_MARKER (an interrupt during the cleanup's logout).
FAKE_GH = """#!/bin/sh
printf '%s|%s\\n' "${GH_CONFIG_DIR-default}" "$*" >> "$GH_CALLS"
case "$1 $2" in
"ssh-key add") [ -z "${HANG_MARKER-}" ] || { : > "$HANG_MARKER"; exec sleep 30; } ;;
"auth logout") [ -z "${HANG_LOGOUT_MARKER-}" ] || { : > "$HANG_LOGOUT_MARKER"; exec sleep 30; } ;;
"auth login") [ -z "${FAIL_LOGIN-}" ] || exit 1; [ -d "$GH_CONFIG_DIR" ] && : > "$GH_CONFIG_DIR/hosts.yml" ;;
esac
exit 0
"""
FAKE_GH_AUTH = """#!/bin/sh
printf 'default|gh-auth.sh\\n' >> "$GH_CALLS"
"""
# A gh-auth.sh at the default ~/.local/share/chezmoi, which a host with another sourceDir must not run.
DECOY_GH_AUTH = """#!/bin/sh
printf 'default|decoy gh-auth.sh\\n' >> "$GH_CALLS"
"""
# The fake chezmoi answers `source-path` with the configured sourceDir's home/ subtree (.chezmoiroot).
FAKE_CHEZMOI = """#!/bin/sh
[ "$1" = source-path ] || exit 2
[ -z "${FAIL_SOURCE_PATH-}" ] || exit 1
printf '%s\\n' "$CHEZMOI_SOURCE_PATH"
"""


class SetupGhTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="setup-gh-test-"))
        self.home = self.temp / "home"
        (self.home / ".ssh").mkdir(parents=True)
        (self.home / ".ssh/id_ed25519.pub").write_text("ssh-ed25519 AAAA fixture\n")
        bin_dir = self.temp / "bin"
        bin_dir.mkdir()
        for name, body in (("gh", FAKE_GH), ("chezmoi", FAKE_CHEZMOI)):
            (bin_dir / name).write_text(body)
            (bin_dir / name).chmod(0o755)
        # The checkout lives at a non-default sourceDir (README: setup.sh reuses a configured sourceDir).
        self.checkout = self.temp / "elsewhere/dotfiles"
        (self.checkout / "home").mkdir(parents=True)
        (self.checkout / "scripts").mkdir()
        git_init(self.checkout, env={"PATH": "/usr/bin:/bin"})
        self.gh_auth = self.checkout / "scripts/gh-auth.sh"
        self.gh_auth.write_text(FAKE_GH_AUTH)
        self.gh_auth.chmod(0o755)
        decoy = self.home / ".local/share/chezmoi/scripts/gh-auth.sh"
        decoy.parent.mkdir(parents=True)
        decoy.write_text(DECOY_GH_AUTH)
        decoy.chmod(0o755)
        self.bin_dir = bin_dir
        self.tmpdir = self.temp / "tmp"
        self.tmpdir.mkdir()
        self.calls = self.temp / "calls"
        self.env = {
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "HOME": str(self.home),
            "TMPDIR": str(self.tmpdir),
            "GH_CALLS": str(self.calls),
            "CHEZMOI_SOURCE_PATH": str(self.checkout / "home"),
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

    def interrupt_at(self, marker_variable: str) -> None:
        """Send TERM, INT and HUP to setup-gh's process group once the fake gh touches the marker; each
        must exit 128 + the signal number with the one-off login's directory removed."""
        for name, number in (("TERM", signal.SIGTERM), ("INT", signal.SIGINT), ("HUP", signal.SIGHUP)):
            with self.subTest(signal=name):
                self.calls.unlink(missing_ok=True)
                marker = self.temp / f"hang-{marker_variable}-{name}"
                process = subprocess.Popen(
                    ["bash", str(SCRIPT)],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env={**self.env, marker_variable: str(marker)},
                    start_new_session=True,
                )
                try:
                    for _ in range(200):
                        if marker.exists() or process.poll() is not None:
                            break
                        subprocess.run(["sleep", "0.05"], check=True)
                    self.assertTrue(marker.exists(), f"the fake gh never reached the {marker_variable} point")
                    # The one-off token is on disk now; the terminal's interrupt reaches the whole group.
                    self.assertEqual(1, len(list(self.tmpdir.glob("*/hosts.yml"))))
                    os.killpg(process.pid, number)
                    returncode = process.wait(timeout=30)
                finally:
                    if process.poll() is None:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                self.assertEqual(128 + number, returncode)
                self.assertEqual([], list(self.tmpdir.iterdir()))
                commands = self.calls.read_text().splitlines()
                self.assertTrue(commands[-1].endswith("|auth logout -h github.com"), commands)
                # The logout runs once: a cleanup re-entered from the trap does not start it again.
                self.assertEqual(1, sum(command.endswith("|auth logout -h github.com") for command in commands))

    def test_a_signal_after_authentication_still_logs_out_and_removes_the_token(self):
        self.interrupt_at("HANG_MARKER")

    def test_a_signal_during_the_logout_still_removes_the_token(self):
        self.interrupt_at("HANG_LOGOUT_MARKER")

    def test_gh_auth_comes_from_the_configured_source_dir_not_the_default(self):
        result, calls = self.run_setup_gh()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(("default", "gh-auth.sh"), calls[0])
        self.assertNotIn(("default", "decoy gh-auth.sh"), calls)

    def test_missing_gh_auth_script_stops_before_any_gh_call(self):
        self.gh_auth.unlink()
        result, calls = self.run_setup_gh()
        self.assertEqual(1, result.returncode)
        self.assertIn(f"{self.checkout}/scripts/gh-auth.sh not found", result.stderr)
        self.assertIn("make gh-auth", result.stderr)
        self.assertEqual([], calls)

    def test_missing_or_failing_chezmoi_stops_before_any_gh_call(self):
        (self.bin_dir / "chezmoi").unlink()
        result, calls = self.run_setup_gh()
        self.assertEqual(1, result.returncode)
        self.assertIn("chezmoi is not installed", result.stderr)
        self.assertEqual([], calls)
        (self.bin_dir / "chezmoi").write_text(FAKE_CHEZMOI)
        (self.bin_dir / "chezmoi").chmod(0o755)
        result, calls = self.run_setup_gh(FAIL_SOURCE_PATH="1")
        self.assertEqual(1, result.returncode)
        self.assertIn("chezmoi source-path failed", result.stderr)
        self.assertEqual([], calls)


if __name__ == "__main__":
    unittest.main()
