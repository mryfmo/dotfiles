"""Exercise make doctor's commit signing key check (scripts/check-tools.sh check_git_signing_key) with real git."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/check-tools.sh"


class CheckSigningKeyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.home = Path(tempfile.mkdtemp(prefix="signing-key-test-"))
        self.gitconfig = self.home / ".gitconfig"

    def tearDown(self) -> None:
        shutil.rmtree(self.home)

    def check(self, config: str, body: str = "check_git_signing_key") -> subprocess.CompletedProcess:
        self.gitconfig.write_text(config)
        env = {
            "PATH": "/usr/bin:/bin:/opt/homebrew/bin",
            "HOME": str(self.home),
            "GIT_CONFIG_GLOBAL": str(self.gitconfig),
            "GIT_CONFIG_NOSYSTEM": "1",
        }
        script = f'source "{SCRIPT}"; {body}; printf "failures=%d\\n" "$required_failures"'
        return subprocess.run(
            ["bash", "-c", script], cwd=self.home, env=env, capture_output=True, text=True, check=False, timeout=30
        )

    def test_missing_signing_key_with_gpgsign_is_a_required_failure(self):
        result = self.check("[user]\n\tsigningkey = ~/.ssh/id_ed25519.pub\n[commit]\n\tgpgsign = true\n")
        self.assertIn("failures=1", result.stdout)
        self.assertIn(f"{self.home}/.ssh/id_ed25519.pub", result.stderr)
        self.assertIn("provision-machine-key", result.stderr)

    def test_present_signing_key_passes(self):
        (self.home / ".ssh").mkdir()
        (self.home / ".ssh/id_ed25519.pub").write_text("ssh-ed25519 AAAA fixture\n")
        result = self.check(f"[user]\n\tsigningkey = {self.home}/.ssh/id_ed25519.pub\n[commit]\n\tgpgsign = true\n")
        self.assertIn("failures=0", result.stdout)
        self.assertIn("found:   commit signing key", result.stdout)

    def test_signing_off_is_not_applicable(self):
        result = self.check("[user]\n\tsigningkey = /nonexistent.pub\n")
        self.assertIn("failures=0", result.stdout)
        self.assertIn("not applicable: commit signing key", result.stdout)

    def test_a_failed_config_read_is_a_required_failure(self):
        # A git that cannot read its config (exit 128 here) is not "signing off".
        result = self.check("[commit]\n\tgpgsign = true\n", body="git() { return 128; }; check_git_signing_key")
        self.assertIn("failures=1", result.stdout)
        self.assertIn("exit 128", result.stderr)

    def test_doctor_runs_the_signing_key_check(self):
        self.assertRegex(SCRIPT.read_text(), r"\n    check_git_signing_key\n")


if __name__ == "__main__":
    unittest.main()
