"""Exercise install/common/credential_dirs.sh: credential directories end at mode 0700 on every apply."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "install/common/credential_dirs.sh"
WRAPPER = ROOT / "home/.chezmoiscripts/common/run_after_08-secure-credential-dirs.sh.tmpl"
DIRS = (".config/gh", ".config/age", ".aws", ".local/share/chezmoi-private")


class CredentialDirsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="credential-dirs-test-"))
        self.home = self.temp / "home"
        self.home.mkdir()
        self.env = {"PATH": "/usr/bin:/bin", "HOME": str(self.home)}

    def tearDown(self) -> None:
        for path in self.temp.rglob("*"):
            if path.is_dir() and not path.is_symlink():
                path.chmod(0o755)
        shutil.rmtree(self.temp)

    def run_script(self, body: str = 'bash "$0"') -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bash", "-c", body, str(SCRIPT)], env=self.env, capture_output=True, text=True, check=False, timeout=30
        )

    def test_group_writable_credential_dirs_become_0700(self):
        for relative in DIRS:
            (self.home / relative).mkdir(parents=True)
            (self.home / relative).chmod(0o775)
        (self.home / ".config/gh").chmod(0o771)
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        for relative in DIRS:
            self.assertEqual(0o700, (self.home / relative).stat().st_mode & 0o777, relative)

    def test_missing_dirs_are_skipped(self):
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse((self.home / ".aws").exists())

    def test_symlink_is_not_followed(self):
        target = self.temp / "shared"
        target.mkdir()
        target.chmod(0o755)
        os.symlink(target, self.home / ".aws")
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(0o755, target.stat().st_mode & 0o777)
        self.assertIn(".aws is a symlink", result.stderr)

    def test_failed_chmod_fails_the_apply_naming_the_dir(self):
        (self.home / ".aws").mkdir()
        result = self.run_script('source "$0"; chmod() { return 1; }; secure_credential_dirs')
        self.assertEqual(1, result.returncode)
        self.assertIn(f"cannot set {self.home}/.aws to mode 0700", result.stderr)

    def test_every_apply_wrapper_runs_the_script(self):
        self.assertTrue(WRAPPER.name.startswith("run_after_"))
        self.assertIn('include "../install/common/credential_dirs.sh"', WRAPPER.read_text())


if __name__ == "__main__":
    unittest.main()
