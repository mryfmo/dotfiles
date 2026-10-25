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

    def test_signing_unset_is_an_optional_notice(self):
        result = self.check("[user]\n\tname = t\n")
        self.assertIn("failures=0", result.stdout)
        self.assertIn("optional warning: commit signing is off", result.stderr)
        self.assertIn("provision-machine-key", result.stderr)

    def test_signing_false_is_not_applicable(self):
        result = self.check("[commit]\n\tgpgsign = false\n")
        self.assertIn("failures=0", result.stdout)
        self.assertIn("not applicable: commit signing key", result.stdout)

    def test_a_failed_config_read_is_a_required_failure(self):
        # A git that cannot read its config (exit 128 here) is not "signing off".
        result = self.check("[commit]\n\tgpgsign = true\n", body="git() { return 128; }; check_git_signing_key")
        self.assertIn("failures=1", result.stdout)
        self.assertIn("exit 128", result.stderr)

    def test_doctor_runs_the_signing_key_check(self):
        self.assertRegex(SCRIPT.read_text(), r"\n    check_git_signing_key\n")


@unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is not installed")
class GitConfigSigningTemplateTest(unittest.TestCase):
    """The managed git config signs commits only when the signing key exists at apply time."""

    def render(self, with_key: bool) -> str:
        with tempfile.TemporaryDirectory(prefix="git-config-template-") as temporary:
            home = Path(temporary)
            if with_key:
                (home / ".ssh").mkdir()
                (home / ".ssh/id_ed25519.pub").write_text("ssh-ed25519 AAAA fixture\n")
            config = home / "chezmoi.toml"
            config.write_text('[data]\nemail = "t@example.invalid"\n')
            result = subprocess.run(
                [
                    str(shutil.which("chezmoi")),
                    "--config",
                    str(config),
                    "--source",
                    str(ROOT / "home"),
                    "--destination",
                    str(home),
                    "execute-template",
                ],
                input=(ROOT / "home/dot_config/git/config.tmpl").read_text(),
                env={"PATH": "/usr/bin:/bin", "HOME": str(home)},
                capture_output=True,
                text=True,
                check=True,
                timeout=60,
            )
            rendered = result.stdout
            self.home = str(home)
        return rendered

    def test_without_the_key_nothing_signing_is_rendered(self):
        rendered = self.render(with_key=False)
        for token in ("gpgsign", "signingkey", "format = ssh"):
            self.assertNotIn(token, rendered)
        self.assertIn("[user]", rendered)

    def test_with_the_key_signing_is_rendered(self):
        rendered = self.render(with_key=True)
        self.assertIn("\tgpgsign = true\n", rendered)
        self.assertIn("\tformat = ssh\n", rendered)
        self.assertIn(f"\tsigningkey = {self.home}/.ssh/id_ed25519.pub\n", rendered)


if __name__ == "__main__":
    unittest.main()
